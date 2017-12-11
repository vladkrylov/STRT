import numpy as np

from subprocess import call
from model.global_coords.data_structures import Event, Track, Hit

class TrackGenerator(object):
    def __init__(self):
        self.mean_ntracks_per_event = 1
        # parameters
        self.phi_mean_sigma = [0.06, 0.15]  # for now taken from analysis of Run25 with MarlinTPC
        self.D0_mean_sigma  = [70., 20.]    # for now taken from analysis of Run25 with MarlinTPC
        
        self.xlim = [0.0, 63.32]
        self.ylim = [40.16, 120.48]
        self.mean_dl = (2.032 + 2.128) / 2.  # collisions per cm, mean of Heed and Degrad simulations
        self.diff_sigma = 0.09
        
        # to be generated
        self.events = []
    

class PythonTrackGenerator(TrackGenerator):
    def __init__(self):
        super(PythonTrackGenerator, self).__init__()
        
    def generate_event(self):
        ev = Event(ev_id=len(self.events), data_file_path=None)
        n_tracks = np.random.poisson(self.mean_ntracks_per_event, 1)[0]
        for i in range(n_tracks):
            ev.add_track(self.generate_track(i))
        ev = self.add_noise(ev)
        self.events.append(ev)
    
    def generate_track(self, track_id):
        D0 = np.random.normal(self.D0_mean_sigma[0], self.D0_mean_sigma[1], 1)[0]
        phi = np.random.normal(self.D0_mean_sigma[0], self.D0_mean_sigma[1], 1)[0]
    
    def add_noise(self, event):
        pass
    
    def save_tracks(self):
        pass
    
    
class HeedTrackGenerator(TrackGenerator):
    def __init__(self):
        super(HeedTrackGenerator, self).__init__()
        
    def generate_events(self, n_events, mean_ntracks_per_event):
        argv = self.D0_mean_sigma + self.phi_mean_sigma + [n_events, mean_ntracks_per_event]
        heed_call_command = "./Heed/edep %s" % (str(argv).replace('[', '').replace(']', '').replace(',', ''))
        print "calling: %s" % heed_call_command
        call(heed_call_command.split())
        
        
if __name__ == "__main__":
    g = HeedTrackGenerator()
    g.generate_events(20, 1.7)
    