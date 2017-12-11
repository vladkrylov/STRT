import math
import numpy as np

eps = 1e-9

def _dist2D(x, y):
    if len(x) != 2 or len(y) != 2:
        return None
    return math.sqrt((x[0]-x[1])**2 + (y[0]-y[1])**2)


def _calc_length(track, _):
    x, y = track.line
    return _dist2D(x, y)


def _calc_phi(track, _):
    x, y = track.line
    if math.fabs(x[1] - x[0]) > eps:
        return math.atan((y[1]-y[0]) / ((x[1]-x[0])))
    else:
        return None


def _calc_D0(track, _):
    x, y = track.line
    if math.fabs(x[1] - x[0]) > eps:
        return ((y[0]*x[1] - y[1]*x[0]) / ((x[1] - x[0])))
    else:
        return None


def _calc_nhits(track, _):
    return len(track.hit_indices)


def _calc_hits_min_dist(track, event):
    d = []
    for i in range(len(track.hit_indices[:-1])):
        i_prev_hit = track.hit_indices[i]
        i_next_hit = track.hit_indices[i+1]
        x = [event.hits[i_prev_hit].x, event.hits[i_next_hit].x]
        y = [event.hits[i_prev_hit].y, event.hits[i_next_hit].y]
        d.append(_dist2D(x, y))
#     d = map(lambda ih: _dist2D([event.hits[ih].x, event.hits[ih+1].x], 
#                                [event.hits[ih].y, event.hits[ih+1].y])
#             , track.hit_indices[:-1])
    return min(d)


def fit_track(track):
    if len(track.hit_indices):
        return None
    x = np.array(track.line[0])
    y = np.array(track.line[1])
    coeffs = np.polyfit(x, y, deg=1)
    
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)
    ybar = np.sum(y)/len(y)
    ssreg = np.sum((yhat-ybar)**2)
    sstot = np.sum((y - ybar)**2)
    r2 = ssreg / sstot
    
    return coeffs, r2
                    
        
track_params_dict = {"Length": _calc_length,
                     "Phi": _calc_phi,
                     "D0": _calc_D0,
                     "Nhits": _calc_nhits,
                     "Dmin": _calc_hits_min_dist}

