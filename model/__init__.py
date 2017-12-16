import os
import cv2
import numpy as np
import time

from model.global_coords.data_structures import *
from savers import RootSaver as Saver
from track_parameters import track_params_dict
from Hough_transform import hough_line_event, Hough_lines_opencv
from model.analysis import fit_Landau
from model.common import generate_run_id

class Model():
    def __init__(self):
        self.runs = []
        self.saver = Saver()
        
    def new_run(self, run_name):
        run_id = generate_run_id(self.runs)
        run = Run(run_id, run_name)
        if run in self.runs:
            return False
        self.runs.append(run)
        return True
    
    def set_run_name(self, run_id, new_name):
        run = [r for r in self.runs if r.id == run_id]
        if len(run) == 0:
            return
        run[0].name = new_name
        
    def add_event(self, run_id, ev):
        run = self.get_run(run_id)
        if ev in run.events:
            return False
        run.events.append(ev)
        return True

    def remove_event(self):
        pass
    
    def add_track(self, run_id, event_id):
        event = self.get_event(run_id, event_id)
        if not event:
            return None
        track_id = self.generate_track_id(event)
        event.add_track(Track(event_id=event_id,
                              track_id=track_id, 
                              track_type="selected"))
        return True
    
    def remove_track(self, run_id, event_id, track_id):
        event, track = self.get_event_and_track(run_id, event_id, track_id)
        if not track or not event:
            return False
        event.tracks.remove(track)
        return True
        
    def add_hits(self, run_id, event_id, track_id, hit_indices):
        event, track = self.get_event_and_track(run_id, event_id, track_id)
        if not track or not event:
            return False
        if not event.hit_indices_are_valid(hit_indices):
            return False
        
        track_index = event.tracks.index(track)
        
        track.add_hits_indices(hit_indices)
        # hits sorting here is lost if it was
        
        event.tracks[track_index] = track
        return True
    
    def remove_hits(self, run_id, event_id, track_id, hit_indices):
        event, track = self.get_event_and_track(run_id, event_id, track_id)
        if not track or not event:
            return False
        if not event.hit_indices_are_valid(hit_indices):
            return False
        
        track_index = event.tracks.index(track)
        
        track.remove_hits_indices(hit_indices)
        # hits sorting here is lost if it was
        
        event.tracks[track_index] = track
        return True
    
    def get_event(self, run_id, event_id):
        run = self.get_run(run_id)
        if run is None or len(run.events) == 0:
            return None
        return filter_by_id(run.events, event_id) or run.events[0]
        
#     def generate_track_id(self, event):
#         existing_ids = [tr.id for tr in event.tracks]
#         if len(existing_ids) == 0:
#             return 0
#         return max(existing_ids) + 1 

    def get_run(self, run_id):
        return filter_by_id(self.runs, run_id)

    def get_event_and_track(self, run_id, event_id, track_id):
        event = self.get_event(run_id, event_id)
        track = None
        if event:
            track = filter_by_id(event.tracks, track_id)
        return event, track

    def save_all(self, where_to_save):
        self.saver.save_all(self.runs, fname=where_to_save)
        print 'Session was stored to %s' % where_to_save
        
    def load_all(self, what_to_load):
        print what_to_load
        self.runs = self.saver.load_all(fname=what_to_load)
        print 'Session was loaded from %s' % what_to_load
        return self.runs[0].id, self.runs[0].events[0].id
    
    def dump_track(self, run_id, event_id, track_id):
        _, track = self.get_event_and_track(run_id, event_id, track_id)
        track.dump()
        
    def get_track_parameters(self):
        return track_params_dict.keys()
        
    def calculate_track_parameters(self):
        pass
#         for ev in self.events:
#             for tr in ev.tracks:
#                 for par_name, calc_function in track_params_dict.iteritems():
#                     tr.parameters[par_name] = calc_function(tr, ev)
    
#     def get_param_distribution(self, parameter_name):
#         return [tr.parameters.get(parameter_name) for ev in self.events 
#                                                   for tr in ev.tracks]
        
    def Hough_transform(self, run_id, event_id, track_id=None):
        event = self.get_event(run_id, event_id)
        _, HT, _, _ = hough_line_event(event, track_id)
        lines = []
        return HT, lines
    
    def analyze_all(self, run_id, parameters):
        run = self.get_run(run_id)
        start = time.time()
        n_tracks = 0
        for ev in run.events:
            self.fast_Hough_transform(run_id, ev.id, parameters)
            n_tracks += len(ev.tracks)
        end = time.time()
        print "============ Reconstruction performance ============="
        print "    %d events analyzed" % len(run.events)
        print "    %d tracks found" % n_tracks
        print "    time elapsed: %.1f seconds" % (end - start)
        
    def fast_Hough_transform(self, run_id, event_id, parameters):
        print "Processing event %d" % event_id
        event = self.get_event(run_id, event_id)
        ########## Pre-HT filters ############
        nhits = len(event.hits)
        if nhits < 50 or nhits > 1600:
            print "Event %d with %d hits was not analyzed, number of hits cut [10, 1000] not passed." % (event_id, nhits)
            return
        ######## End pre-HT filters ##########
        event.tracks = []
        event.reconstructed_hit_indices = []
        for i_Hough in range(4):
            Hough_lines_opencv(event, parameters)
            for _ in range(5):
                self.filter_close_tracks(event)
                for t in event.tracks:
                    if len(t.hit_indices) > 0:
                        self.handle_empty_gaps(event, t)
                    else:
                        event.tracks.remove(t)
                self.handle_shared_hits(event)
            for t in event.tracks:
                event.reconstructed_hit_indices.extend(t.hit_indices)
            
        ########## Post-HT filters ############
        bad_tracks = []
        for t in event.tracks:
            if t.length() < 10:
                bad_tracks.append(t)
                continue
            if float(len(t.hit_indices)) / t.length() < 0.7:
                bad_tracks.append(t)
                continue
            if t.length() < 20 and float(len(t.hit_indices)) / t.length() < 1.4:
                bad_tracks.append(t)
                continue
        event.tracks = [t for t in event.tracks if t not in bad_tracks]
        if len(event.tracks) > 10:
            event.tracks = []
        ######## End post-HT filters ##########
        event.reconstructed_hit_indices = []
        for t in event.tracks:
            t.is_good = self.track_is_good(t)
            event.reconstructed_hit_indices.extend(t.hit_indices)

    def filter_close_tracks(self, event):
        # situation when large track contains small track is not handled properly
        similarity_thr = 0.8
        repeated_tracks = []
        for i in range(len(event.tracks)):
            t1 = event.tracks[i]
            if t1 in repeated_tracks:
                continue
            for j in range(i+1, len(event.tracks)):
                t2 = event.tracks[j]
                if t1.similar_to(t2) > similarity_thr:
                    repeated_tracks.append(t2)
        event.tracks = [t for t in event.tracks if t not in repeated_tracks]
    #             print "Similarity between %d and %d = %f" % (t1.id, t2.id, t1.similar_to(t2))
    #             print "Fast similarity between %d and %d = %f" % (t1.id, t2.id, t1.fast_similar_to(t2))

    def handle_shared_hits(self, event):
        for i in range(len(event.tracks)):
            t1 = event.tracks[i]
            for j in range(i+1, len(event.tracks)):
                t2 = event.tracks[j]
                common_hits = set(t1.hit_indices) & set(t2.hit_indices)
                for ih in common_hits:
                    k1 = t1.hit_indices.index(ih)
                    k2 = t2.hit_indices.index(ih)
                    
#                     txs = [24.3225, 24.346]
#                     tys = [81.9915, 82.0477]
#                     h = event.hits[ih]
#                     if h.x > txs[0] and h.x < txs[1] \
#                     and h.y > tys[0] and h.y < tys[1]:
#                         print 'Hit at (%.3f, %.3f):' % (h.x, h.y)
#                         print 'Track%d residual = %.4f' % (t1.id, np.fabs(t1.residuals[k1]))
#                         print 'Track%d residual = %.4f' % (t2.id, np.fabs(t2.residuals[k2]))
                    
                    if np.fabs(t1.residuals[k1]) > np.fabs(t2.residuals[k2]):
                        t1.remove_hit(ih)
                    else:
                        t2.remove_hit(ih)
                assert(len(t1.hit_indices) == len(t1.lincoor))
                assert(len(t1.hit_indices) == len(t1.residuals))
                assert(len(t2.hit_indices) == len(t2.lincoor))
                assert(len(t2.hit_indices) == len(t2.residuals))

    def handle_empty_gaps(self, event, track):
        subtracks = [[track.hit_indices[0]]]
        max_distance_thr = 10.;
        for i in range(1, len(track.hit_indices)):
            if np.fabs(track.lincoor[i] - track.lincoor[i-1]) > max_distance_thr:
                subtracks.append([track.hit_indices[i]])
            else:
                subtracks[-1].append(track.hit_indices[i])
        i_max_subtrack = subtracks.index(max(subtracks, key=lambda st: len(st)))
        track.hit_indices = subtracks[i_max_subtrack]
        track.fit(event)
        for i in range(len(subtracks)):
            if i == i_max_subtrack or len(subtracks[i]) == 0:
                continue
            t = Track(event_id=event.id, 
                      track_id=len(event.tracks),
                      track_type="reconstructed")
            t.add_hits_indices(subtracks[i])
            t.fit(event)
            event.add_track(t)
#         print "Track %d has %d subtracks" % (track.id, len(subtracks))

    def mark_good_track(self, run_id, event_id, track_id, is_good):
        _, track = self.get_event_and_track(run_id, event_id, track_id)
        track.is_good = is_good
        
    def track_is_good(self, tr):
        if tr.length() < 47.:
            return False
            
        n_hits = len(tr.hit_indices)
        if n_hits < 47:
            return False
            
        density = float(n_hits) / tr.length()
        if density < 1.12 or density > 4.:
            return False
        
        start_point = tr.get_start_point()   
        if start_point[0] > 14.:
            return False
            
        if tr.theta < -0.2 or tr.theta > 0.35:
            return False
            
        if tr.rho < 55. or tr.theta > 0.35 \
        or (tr.rho > 69.5 and tr.rho < 77.8):
            return False
        
        return True

    def dump2matlab(self, run_id):
        pass
#         '''Exports reconstructed tracks sttistics to the Matlab file for producing a nice plots.
#         The same should be done using Matplolib in future.
#         '''
#         print "Matlab dump"
#         with open('STRT_matlab.m', 'w') as mfile:
#             mfile.write('clear all;\n')
#             mfile.write('good_tracks_length = %s;\n'
#                         % str([t.length() for ev in self.events for t in ev.tracks
#                                           if t.is_good]))
#             mfile.write('bad_tracks_length = %s;\n'
#                         % str([t.length() for ev in self.events for t in ev.tracks
#                                           if not t.is_good]))
#             mfile.write('good_tracks_rho = %s;\n'
#                         % str([t.rho for ev in self.events for t in ev.tracks
#                                      if t.is_good]))
#             mfile.write('bad_tracks_rho = %s;\n'
#                         % str([t.rho for ev in self.events for t in ev.tracks
#                                      if not t.is_good]))
#             mfile.write('good_tracks_theta = %s;\n'
#                         % str([t.theta for ev in self.events for t in ev.tracks
#                                        if t.is_good]))
#             mfile.write('bad_tracks_theta = %s;\n'
#                         % str([t.theta for ev in self.events for t in ev.tracks
#                                        if not t.is_good]))
#             mfile.write('good_tracks_x0 = %s;\n'
#                         % str([t.start_point[0] for ev in self.events for t in ev.tracks
#                                                 if t.is_good]))
#             mfile.write('bad_tracks_x0 = %s;\n'
#                         % str([t.start_point[0] for ev in self.events for t in ev.tracks
#                                                 if not t.is_good]))
#             mfile.write('good_tracks_y0 = %s;\n'
#                         % str([t.start_point[1] for ev in self.events for t in ev.tracks
#                                                 if t.is_good]))
#             mfile.write('bad_tracks_y0 = %s;\n'
#                         % str([t.start_point[1] for ev in self.events for t in ev.tracks
#                                                 if not t.is_good]))
#             good_tracks_Nhits = [len(t.hit_indices) for ev in self.events for t in ev.tracks
#                                                     if t.is_good]
#             mfile.write('good_tracks_Nhits = %s;\n' % str(good_tracks_Nhits))
#             mfile.write('bad_tracks_Nhits = %s;\n'
#                         % str([len(t.hit_indices) for ev in self.events for t in ev.tracks
#                                                   if not t.is_good]))
#             mfile.write('good_tracks_R2 = %s;\n'
#                         % str([t.R2 for ev in self.events for t in ev.tracks
#                                     if t.is_good]))
#             mfile.write('bad_tracks_R2 = %s;\n'
#                         % str([t.R2 for ev in self.events for t in ev.tracks
#                                     if not t.is_good]))
#             n_good_tracks = len(good_tracks_Nhits)
#             max_N_hits = max(good_tracks_Nhits)
#             mfile.write('lincoords = NaN(%d, %d);\n' % (n_good_tracks, max_N_hits))
#             tracks_counter = 0
#             for ev in self.events:
#                 for t in ev.tracks:
#                     if t.is_good:
#                         tracks_counter += 1
#                         mfile.write('lincoords(%d, 1:%d) = %s;\n' % (tracks_counter,
#                                                                      len(t.hit_indices),
#                                                                      str(t.lincoor))
#                                     )
#             mfile.write('save(Runtracks.mat);\n')

    def plot_dEdx(self, run_id, gap, nbins):
        run = self.get_run(run_id)
        if run is None:
            return None
        dN = np.array([])
        for ev in run.events:
            for t in ev.tracks:
                if not t.is_good:
                    continue
                bin_edges = np.arange(np.amin(t.lincoor), np.amax(t.lincoor), gap)
                N, _ = np.histogram(t.lincoor, bins=bin_edges)
                dN = np.concatenate((dN, N))
        fit_Landau(dN, gap)
        with open('dEdx.txt', 'w') as out_file:
            out_file.write('gap_length = %f;' % gap)
            out_file.write('dEdx = %s;' % str(dN))


            