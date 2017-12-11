class Event():
    def __init__(self, ev_id):
        self.id = ev_id
        self.hits = []
        
    def add_hit(self, hit):
        self.hits.append(hit)
    

class Hit():
    def __init__(self):
        pass
    
    def __repr__(self):
        pass
        
        
class Track():
    def __init__(self):
        pass
    
