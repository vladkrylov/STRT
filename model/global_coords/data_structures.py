import numpy as np

from random import uniform
from model.common import filter_by_id
from model.color_set import get_color
from model.track_parameters import track_params_dict
from scipy.ndimage.morphology import binary_hit_or_miss

class Event():
    def __init__(self, ev_id, data_file_path):
        self.path = data_file_path
        self.id = ev_id
        self.hits = []
        self.reconstructed_hit_indices = []
        self.tracks = []
        # these are needed for event-image-event conversion
        self.pixelize_step = 0.055
        self.xmin = None
        self.xmax = None
        self.ymin = None
        self.ymax = None
        
    def __repr__(self):
        return "Event %d with %d hits" % (self.id, len(self.hits))
    
    def __eq__(self, other):
        return self.id == other.id
#         return self.path == other.path
    
    def __neq__(self, other):
        return not self.__eq__(other)
        
    def add_hit(self, hit):
        self.hits.append(hit)
        if hit.x < self.xmin or self.xmin is None:
            self.xmin = hit.x
        if hit.x > self.xmax or self.xmax is None:
            self.xmax = hit.x
        if hit.y < self.ymin or self.ymin is None:
            self.ymin = hit.y
        if hit.y > self.ymax or self.ymax is None:
            self.ymax = hit.y
        
    def add_track(self, new_track):
        self.tracks.append(new_track)
        
    def get_track(self, track_id):
        return filter_by_id(self.tracks, track_id)
    
    def hit_indices_are_valid(self, hit_indices):
        out_of_range = filter(lambda i: i >= len(self.hits), hit_indices)
        if len(out_of_range) == 0:
            return True
        return False
    
    def get_bin_image(self):
        binary_one = 255
        
        xs = [int(self.hits[i].x/self.pixelize_step) for i in range(len(self.hits)) if i not in self.reconstructed_hit_indices]
        ys = [int(self.hits[i].y/self.pixelize_step) for i in range(len(self.hits)) if i not in self.reconstructed_hit_indices]
        if len(xs) == 0:
            return None, None, None, None
        
        xmin = min(xs)
        xmax = max(xs)
        ymin = min(ys)
        ymax = max(ys)
        bin_img = np.zeros((ymax-ymin+1, xmax-xmin+1), dtype=np.uint8)
        for i in range(len(xs)):
            xp = xs[i] - xmin
            yp = ymax - ys[i]
            bin_img[yp, xp] = binary_one
            
        return bin_img, self.pixelize_step, (xmin, xmax), (ymin, ymax)
    
    def line_to_track(self, Hough_line):
        if self.xmin is None or self.ymax is None:
            return None
        
        rho, theta = Hough_line
        rho = self.ymax - 1/np.tan(theta) * (self.xmin + self.pixelize_step * rho / np.cos(theta))
        theta = np.pi/2 - theta
        
        return 
    
    def adjust_track(self, line, sigmaXY):
        rho, theta = line
        rho = self.ymax - 1/np.tan(theta) * (self.xmin + self.pixelize_step*rho/np.cos(theta))
        theta = np.pi/2 - theta
        old_inds = []
        new_inds = [i for i, h in enumerate(self.hits) if h.belongs_to_line(np.array([rho, theta]), sigmaXY)]
        counter = 20
        while old_inds != new_inds and counter != 0:
            counter -= 1
            old_inds = list(new_inds)
            if len(old_inds) == 0:
                return None
            
            x = [self.hits[i].x for i in old_inds]
            y = [self.hits[i].y for i in old_inds]
            coeffs = np.polyfit(x, y, 1)
            rho, theta = np.array([coeffs[1], np.arctan(coeffs[0])])
            new_inds = [i for i, h in enumerate(self.hits) if h.belongs_to_line(np.array([rho, theta]), sigmaXY)]
        new_id = 0
        if len(self.tracks) > 0:
            new_id = max([t.id for t in self.tracks])+1
        t = Track(event_id=self.id, 
                  track_id=new_id,
                  track_type="reconstructed")
        t.add_hits_indices(new_inds)
        track_hits = [self.hits[i] for i in t.hit_indices]
        if len(track_hits) == 0:
            return None
        
        t.fit(self)
        self.add_track(t)
        return t
        
class Hit():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __repr__(self):
        return "Hit at %f\t%f" % (self.x, self.y)
    
    def belongs_to_line(self, line, sigmaXY):
        rho, theta = line
        y_expected = rho + np.tan(theta)*self.x
        dy = sigmaXY/np.cos(theta)
        return self.y < (y_expected+dy) and self.y > (y_expected-dy)
        
        
class Track():
    def __init__(self, event_id, track_id, track_type="selected", color=None):
        self.hit_indices = []
        self.event_id = event_id
        self.is_good = False
        self.id = track_id
        self.type = track_type
        self.line = None
        self.rho = None
        self.theta = None
        self.R2 = None
        self.start_point = None
        self.lincoor = []
        self.residuals = []
        self.displayed = True
        if color:
            self.color = color
        else:
            try:
                self.color = get_color(self.id)
            except:
                self.color = '#00ff00'
        self.parameters = {}
        
    def __repr__(self):
        return "Track %d with %d hits" % (self.id, len(self.hit_indices))
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __neq__(self, other):
        return not self.__eq__(other)
    
    def dump(self):
        dump_str = "Track %d\n" % self.id
        dump_str += "    length = %.2f\n" % self.length()
        dump_str += "    rho    = %.2f\n" % self.rho
        dump_str += "    theta  = %.2f\n" % self.theta
        dump_str += "    start  = %.2f, %.2f\n" % self.start_point
        dump_str += "    N_hits = %d\n"   % len(self.hit_indices)
        dump_str += "    R^2    = %.2f\n" % self.R2
        print dump_str
    
    def add_hits_indices(self, hit_indices):
        self.hit_indices = list(set(self.hit_indices).union(set(hit_indices)))
        
    def remove_hits_indices(self, hit_indices):
        '''After adding and sorting the self.lincoords and self.residuals this doesn't work anymore'''
        self.hit_indices = list(set(self.hit_indices) - set(hit_indices))
    
    def remove_hit(self, hit_index):
        i = self.hit_indices.index(hit_index)
        self.hit_indices.pop(i)
        if self.lincoor is not None:
            self.lincoor.pop(i)
        if self.residuals is not None:
            self.residuals.pop(i)
         
    def set_random_line(self, xlims, ylims):
        x_min, x_max = xlims
        y_min, y_max = ylims
        
        if x_min > 0 and x_max > 0:
            length = x_max - x_min
            x_min += 0.1 * length
            x_max -= 0.1 * length
        elif x_min < 0 and x_max > 0:
            length = x_max - x_min
            x_min += 0.1 * length
            x_max -= 0.1 * length
        elif x_min < 0 and x_max < 0:
            length = x_min - x_max
            x_min -= 0.1 * length
            x_max += 0.1 * length
        else:
            # means x_min > x_max, nonsense
            pass 
        x = [x_min, x_max]
        y = [uniform(y_min, y_max)] * 2
        self.set_line(x, y)
    
    def set_line(self, xs, ys):
        self.line = (xs, ys)
    
    def has_line(self):
        return self.line is not None and len(self.line) == 2
    
    def length(self):
        if len(self.lincoor) > 2:
            return self.lincoor[-1] - self.lincoor[0]
        else:
            return 0.
    
    def similar_to(self, other):
        l1 = len(self.hit_indices)
        l2 = len(other.hit_indices)
        if l1 == 0 or l2 == 0:
            return 0.
        
        hits_common = set(self.hit_indices) & set(other.hit_indices)
        return float(len(hits_common))/min(l1, l2)
    
    def mark_as_good(self):
        self.is_good = True
        
    def mark_as_bad(self):
        self.is_good = False
        
#         hit_diff = set(self.hit_indices).symmetric_difference(set(other.hit_indices))
#         return 1 - float(len(hit_diff)) / (l1 + l2)
    
#     def fast_similar_to(self, other):
#         phi1 = self.parameters.get('Phi')
#         phi2 = other.parameters.get('Phi')
#         D01 = self.parameters.get('D0')
#         D02 = other.parameters.get('D0')
#         
#         if phi1 is None or phi2 is None \
#         or D01 is None or D02 is None:
#             return 0.
#         
#         return np.fabs(phi2 - phi1) * np.fabs(D02 - D01)
    
    def distance_to_hit(self, hit):
        if self.theta is None or self.rho is None:
            return None
        k = self.rho / np.cos(self.theta)
        m = np.tan(self.theta)
        return np.fabs(k + m*hit.x - hit.y) / np.sqrt(1 + m*m)

    def fit(self, event):
        hits = np.array([[event.hits[i].x, event.hits[i].y]  for i in self.hit_indices])
        coeffs = np.polyfit(hits[:,0], hits[:,1], 1)
        self.theta = np.arctan(coeffs[0])
        self.rho = coeffs[1]*np.cos(self.theta)
        
        xline = [np.amin(hits[:,0]), np.amax(hits[:,0])]
        yline = [coeffs[1] + coeffs[0]*x for x in xline]
        self.set_line(xline, yline)
        
        th = np.arctan(coeffs[0])
        rotation_matrix = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        transformed_hits = hits.dot(rotation_matrix)
#         self.lincoor = transformed_hits[:,0].tolist()
#         self.residuals = np.fabs(transformed_hits[:,1]).tolist()
        # sort transformed coordinates
        # and rearrange hit_indices accordingly
#         dtype = [('lin_coords', float), ('residuals', float), ('hit_indices', int)]
        lincoor = transformed_hits[:,0]
        sorted_inds = np.argsort(lincoor)
        self.hit_indices = np.array(self.hit_indices)[sorted_inds].tolist()
        self.lincoor = lincoor[sorted_inds]
        self.lincoor = (self.lincoor - self.lincoor[0]).tolist()
        residuals = transformed_hits[:,1][sorted_inds] - self.rho
        self.residuals = residuals.tolist()
        self.R2 = np.sum(np.power(residuals, 2)) / len(self.hit_indices)
        first_hit = event.hits[self.hit_indices[0]]
        self.start_point = (first_hit.x, first_hit.y)
        

        
        