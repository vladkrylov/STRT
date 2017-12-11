import yaml

from model import Track

track_file = "../outdata/Run25/tracks.yaml"

data = None
with open(track_file, 'r') as trfile:
    data = trfile.read()

raw_tracks = data.split("---")
tracks = [yaml.load(t) for t in raw_tracks if t.split()]

print tracks
    
