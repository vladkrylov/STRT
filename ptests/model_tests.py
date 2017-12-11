from unittest import TestCase
from random import randint
from model import Model, Event, Track, Hit

def generate_event(max_possible_id, ev_id=None):
    if ev_id is None:
        ev_id = randint(0, max_possible_id)
        
    ev = Event("/some/dummy/path%d" % ev_id)
    ev.id = ev_id
    return ev

class TestModelAPI(TestCase):
    def aux(self):
        self.m = Model()
        
        self.add_event = self.m.add_event
        self.add_track = self.m.add_track
        self.remove_track = self.m.remove_track
        self.add_hits = self.m.add_hits
        
    def test_add_events(self):
        self.aux()
        event_ids = [4, 4, 8, 2, 4, 2, 3, 6, 7, 0, 10, 4, 0, 4, 4, 5, 2, 8, 10, 3]
        
        for ev_id in event_ids:
            ev = generate_event(None, ev_id)
            self.add_event(ev)
        
        loaded_events = [ev.id for ev in self.m.events]
        should_be = [4, 8, 2, 3, 6, 7, 0, 10, 5]
        self.assertEqual(should_be, loaded_events)
        
    def test_add_remove_track(self):
        self.aux()
        
        ev_id = 17
        ev = generate_event(None, ev_id)
        self.add_event(ev)
        
        self.add_track(ev_id)
        self.add_track(ev_id)
        self.add_track(ev_id)
        self.add_track(ev_id)
        
        self.remove_track(ev_id, 2)
        
        added_track_ids = [tr.id for tr in self.m.events[0].tracks]
        expected_track_ids = [0, 1, 3]
        self.assertEqual(added_track_ids, expected_track_ids)
        
    def test_add_remove_hits(self):
        self.aux()
        
        ev_id = 21
        ev = generate_event(None, ev_id)
        
        test_hit_coords = [(58.5, 44.3), (39.2, 63.8), (11.4, 78.1), (58.6, 24.8), (26.9, 59.9), (13.6, 75.4), (8.6, 52.9), (55.6, 28.3), (0.6, 71.1), (9.2, 22.8), (62.9, 57.6), (38.1, 64.7), (51.5, 4.0), (32.1, 65.3), (8.7, 35.6), (42.7, 17.1), (34.2, 41.6), (55.6, 4.7), (12.1, 40.7), (23.4, 65.3), (39.0, 27.9), (5.3, 44.6), (27.0, 60.6), (60.5, 29.0), (49.8, 55.5), (29.9, 11.4), (60.6, 53.8), (57.5, 58.0), (23.7, 3.7), (32.1, 15.6), (33.1, 3.5), (17.0, 12.5), (59.7, 49.3), (19.7, 53.5), (35.3, 44.5), (2.1, 43.4), (37.6, 56.8), (46.0, 23.6), (6.7, 25.9), (46.0, 53.9), (46.6, 18.6), (58.7, 41.2), (34.8, 75.0), (46.4, 1.7), (5.5, 37.6), (62.0, 45.4), (20.8, 68.8), (43.2, 45.0), (48.7, 15.5), (31.9, 47.8)]
        for x, y in test_hit_coords:
            ev.add_hit(Hit(x, y))
        
        track0 = Track(track_id=0, track_type="selected")
        track1 = Track(track_id=1, track_type="recognized")
        
        track0.add_hits_indices(range(0, 15))
        track0.add_hits_indices(range(3, 10))
        track0.add_hits_indices(range(11, 17))
        
        track1.add_hits_indices(range(19, 35))
        track1.add_hits_indices(range(21, 26))
        track1.remove_hits_indices(range(23, 29))
        
        ev.add_track(track0)
        ev.add_track(track1)
        
        self.add_event(ev)
        
        # use sets here since add/remove hits mixes up the existing indices
        track0_hit_inds = set(self.m.get_event(ev_id).get_track(0).hit_indices)
        expected_track0_hit_inds = set(range(0, 17))
        self.assertEqual(len(track0_hit_inds ^ expected_track0_hit_inds), 0)
        
        track1_hit_inds = set(self.m.get_event(ev_id).get_track(1).hit_indices)
        expected_track1_hit_inds = set(range(19, 23) + range(29, 35))
        self.assertEqual(len(track1_hit_inds ^ expected_track1_hit_inds), 0)
        

        