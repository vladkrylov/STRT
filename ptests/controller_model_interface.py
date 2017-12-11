from controller import Controller
from model import Model
from model_tests import TestModelAPI

class TestControllerModelInterface(TestModelAPI):
    
    def aux(self):
        self.m = Model()
        self.c = Controller(self.m, None)
        
        # substitute the model manipulation with controller API
        self.add_event = self.c.on_event_loaded
        
        self.add_track = self.c.on_add_track
        self.remove_track = self.c.on_remove_track
        
        self.add_hits = self.c.on_add_hits
        self.remove_hits = self.c.on_remove_hits
        
