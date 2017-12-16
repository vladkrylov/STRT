import yaml
import os

import ROOT as r
from model import Run, Event, Track, Hit
from model.common import generate_run_id, filter_by_id
from model.color_set import get_color

# import rootpy
from rootpy.tree import Tree, TreeModel, IntCol, FloatCol
from rootpy.io import root_open, DoesNotExist
from rootpy import stl
from random import gauss

class Saver():
    def __init__(self):
        self.file = None

    def is_open(self):
        pass

    def save_track(self, track):
        pass


class YamlSaver():
    def __init__(self, directory):
        self.directory = os.path.abspath(directory)
        if not os.path.exists(self.directory):
            raise Exception("Directory %s dos not exist" % self.directory)
        self.track_file = os.path.join(self.directory, "tracks.yaml")
        self.event_file = os.path.join(self.directory, "events.yaml")

    def save_track(self):
        pass

    def save_all(self, events):
        with open(self.event_file, 'w') as evfile:
            for e in events:
                evfile.write(self.dump_event(e))
        with open(self.track_file, 'w') as trfile:
            for e in events:
                for t in e.tracks:
                    trfile.write(self.dump_track(t))
                    trfile.write("---\n")
                        
    def load_all(self):
        with open(self.event_file, 'r') as evfile:
            data = evfile.read()
            events = []
        raw_events = data.split("# New Event")
        for e in raw_events:
            if len(e) > 0:
                ev_dict = yaml.load(e)
                ev_id = ev_dict["id"]
                new_event = Event(ev_id, self.directory)
                xhits = ev_dict["xhits"]
                yhits = ev_dict["yhits"]
                new_event.hits = [Hit(x, y) for x, y in zip(xhits, yhits)]
                events.append(new_event)
        
        with open(self.track_file, 'r') as trfile:
            data = trfile.read()
        raw_tracks = data.split("---")
        tracks = [yaml.load(t) for t in raw_tracks if t.split()]
        for t in tracks:
            t.displayed = True
            t.parameters = {}
            if not hasattr(t, "color"):
                t.color = get_color(t.id)
            event_id = t.event_id
            filt_events = filter(lambda ev: ev.id == event_id, events)
            if len(filt_events) > 0:
                event = filt_events[0]
                event.add_track(t)
        return events

    def dump_event(self, event):
        x = [hit.x for hit in event.hits]
        y = [hit.y for hit in event.hits]
        
        props_list = []
        # TODO generate the header accordingly
#         props_list.append("!!python/object:model.global_coords.data_structures.Event")
        props_list.append("# New Event")
        props_list.append("id: %d" % event.id)
#         props_list.append('path: "%s"' % event.path)
        props_list.append("xhits: %s" % x)
        props_list.append("yhits: %s" % y)
        return '\n'.join(props_list) + '\n'

    def dump_track(self, track):
        props_list = []
        # TODO generate the header accordingly
        props_list.append("!!python/object:model.global_coords.data_structures.Track")
        props_list.append("id: %d" % track.id)
        props_list.append("event_id: %d" % track.event_id)
        props_list.append('color: "%s"' % track.color)
        props_list.append('length: %.2f' % track.length())
        props_list.append('rho: %.2f' % track.rho)
        props_list.append('theta: %.2f' % track.theta)
        props_list.append('start: (%.2f, %.2f)' % track.get_start_point())
        props_list.append('N_hits: %d' % len(track.hit_indices))
        props_list.append('R^2: %.2f' % track.R2)
        props_list.append('is_good: %r' % track.is_good)
        props_list.append("hit_indices: %s" % track.hit_indices)
        props_list.append("line: !!python/tuple\n- %s\n- %s\n" % (track.line[0], track.line[1]))
        return '\n'.join(props_list)


class RootSaver():
    class rEvent(TreeModel):
        id = IntCol()
        xhits = stl.vector("float")
        yhits = stl.vector("float")
        nHits = IntCol()
        nTracks = IntCol()
        nGoodTracks = IntCol()
        
    class rTrack(TreeModel):
        id = IntCol()
        event_id = IntCol()
        hit_indices = stl.vector("int")
        color = IntCol()
        length = FloatCol()
        rho = FloatCol()
        theta = FloatCol()
        x0 = FloatCol()
        y0 = FloatCol()
        x1 = FloatCol()
        y1 = FloatCol()
        nHits = IntCol()
        R2 = FloatCol()
        is_good = IntCol()
        
    def __init__(self):
        pass
    
    def save_all(self, runs, fname='strt_session.root'):
        with root_open(fname, 'recreate') as root_file:
#             d1 = root_file.mkdir('Test1')
#             d1.cd()
#             ntuple = Ntuple(('a', 'b', 'c'), name="test")
#             for i in range(20):
#                 ntuple.Fill(gauss(.5, 1.), gauss(.3, 2.), gauss(13., 42.))
#             ntuple.write()
            for run in runs:
                run_dir = root_file.mkdir(run.name)
                run_dir.cd()
                event_tree = Tree('Events', model=RootSaver.rEvent)
                track_tree = Tree('Tracks', model=RootSaver.rTrack)
                for event in run.events:
                    event_tree.id = event.id
                    for i in range(len(event.hits)):
                        event_tree.xhits.push_back(event.hits[i].x)
                        event_tree.yhits.push_back(event.hits[i].y)
                    event_tree.nHits = len(event.hits)
                    event_tree.nTracks = len(event.tracks)
                    event_tree.nGoodTracks = len([t for t in event.tracks if t.is_good])
                    event_tree.fill(reset=True)
                    
                    for track in event.tracks:
                        track_tree.id = track.id
                        track_tree.event_id = track.event_id
                        for i in track.hit_indices:
                            track_tree.hit_indices.push_back(i)
                        track_tree.color = track.int_color()
                        track_tree.length = track.length()
                        track_tree.rho = track.rho
                        track_tree.theta = track.theta
                        track_tree.x0 = track.get_start_point()[0]
                        track_tree.y0 = track.get_start_point()[1]
                        track_tree.x1 = track.get_end_point()[0]
                        track_tree.y1 = track.get_end_point()[1]
                        track_tree.nHits = len(track.hit_indices)
                        track_tree.R2 = track.R2
                        track_tree.is_good = track.is_good
                        track_tree.fill(reset=True)
                event_tree.write()
                track_tree.write()
                
    def load_all(self, fname='strt_session.root'):
        full_fname = os.path.abspath(fname)
        if not os.path.exists(full_fname):
            print 'File %s does not exists.' % full_fname
            return
        runs = []
        with root_open(full_fname) as root_file:
            directories = next(root_file.walk())[1]
            for dir in directories:
                run_id = generate_run_id(runs)
                run = Run(run_id, name=dir)
                event_tree = root_file.Get(dir).Get('Events')
                track_tree = None
                try:
                    track_tree = root_file.Get(dir).Get('Tracks')
                except DoesNotExist:
                    pass
                for event in event_tree:
                    e = Event(ev_id=event.id, data_file_path='')
                    for i in range(event.xhits.size()):
                        h = Hit(event.xhits[i], event.yhits[i])
                        e.hits.append(h)
                    run.events.append(e)
                    
                current_event = run.events[0]
                for track in track_tree:
                    ev_id = track.event_id
                    if ev_id != current_event.id:
                        current_event = filter_by_id(run.events, ev_id)
                    t = Track(ev_id, track.id)
                    for i in track.hit_indices:
                        t.hit_indices.append(i)
                    t.color_from_int(track.color)
                    t.rho = track.rho
                    t.theta = track.theta
                    t.set_line((track.x0, track.x1), (track.y0, track.y1))
                    t.R2 = track.R2
                    t.is_good = track.is_good
                    t.calculate_parameters(current_event)
                    current_event.tracks.append(t)
                    
                runs.append(run)
        print '%d runs were loaded' % len(runs)
        return runs

if __name__ == "__main__":
    from model import Event, Track
    with open("../outdata/Run25/tracks.yaml", 'r') as tracks:
        data = tracks.read()
        for t in yaml.load_all(data):
            print t





    