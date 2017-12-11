# taken from https://github.com/alyssaq/hough_transform/blob/master/hough_transform.py

import cv2
import numpy as np
import matplotlib.pyplot as plt

from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion


def hough_line_event(event, track_id=None, angle_step=1):
    """
    Hough transform for lines
    Input:
    event - Event class object from model.global_coords.data_structures
    angle_step - Spacing between angles to use every n-th angle
      between -90 and 90 degrees. Default step is 1.
    Returns:
    accumulator - 2D array of the hough transform accumulator
    theta - array of angles used in computation, in radians.
    rhos - array of rho values. Max size is 2 times the diagonal
           distance of the input image.
    """
    pixelize_step = 0.055
    rho_scale = 20
     
    xs = [int(h.x/pixelize_step / rho_scale) for h in event.hits]
    ys = [int(h.y/pixelize_step / rho_scale) for h in event.hits]
    xmin = min(xs)
    xmax = max(xs)
    ymin = min(ys)
    ymax = max(ys)
     
    track = event.get_track(track_id)
    if track is not None:
        xs = map(lambda i: xs[i], track.hit_indices)
        ys = map(lambda i: ys[i], track.hit_indices)
     
    # Rho and Theta ranges
    thetas = np.deg2rad(np.arange(-90.0, 90.0, angle_step))
    width = xmax - xmin
    height = ymax - ymin
    diag_len = np.ceil(np.sqrt(width * width + height * height))
    rhos = np.linspace(-diag_len, diag_len, diag_len)
     
    # Cache some reusable values
    cos_t = np.cos(thetas)
    sin_t = np.sin(thetas)
    num_thetas = len(thetas)
     
    # Hough accumulator array of theta vs rho
    accumulator = np.zeros((2*diag_len+1, num_thetas), dtype=np.uint64)
    y_idxs, x_idxs = ys, xs
     
    # Vote in the hough accumulator
    for i in range(len(x_idxs)):
        x = x_idxs[i] - xmin
        y = y_idxs[i] - ymin
      
        for t_idx in range(num_thetas):
            # Calculate rho. diag_len is added for a positive index
            rho = round(x * cos_t[t_idx] + y * sin_t[t_idx]) + diag_len
#             rho_inds.append(rho)
            accumulator[rho, t_idx] += 1
    lines = None
    

    
#     return None, None, None, None
    return lines, accumulator, thetas, rhos


def dump_lines(event):
    bin_img, pixelize_step, _, _ = event.get_bin_image()
    lines = cv2.HoughLines(image=bin_img, rho=1, theta=np.pi/180, threshold=10)
    if lines is None:
        lines = []
    else:
        for l in lines:
            # retain rho units
            l[0, 0] *= pixelize_step
            l[0, 1] += np.pi
    
    dst = np.zeros(shape=bin_img.shape)
    norm_bin_img = cv2.normalize(bin_img, dst, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    
    return lines


def add_lines_to_image(img, lines, dump=True):
    img_res = img.copy()
    for l in lines:
        rho, theta = l[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
    
        cv2.line(img_res, (x1,y1), (x2,y2), (255,255,255), 2)

    if dump:
        cv2.imwrite('houghlines.jpg', img_res)
        
    return img_res


def plot_image(img):
    plt.imshow(img, interpolation='nearest', aspect='auto')


def plot_event(event):
    points = [(h.x, h.y) for h in event.hits]
    x = map(lambda point: point[0], points)
    y = map(lambda point: point[1], points)
    plt.plot(x, y, 'k.')


def make_me_happy(event, rho_step=2, theta_step=np.pi/90, thr=100):
    if len(event.hits) == 0:
        return None
    
    bin_img, _, _, _ = event.get_bin_image()
    if bin_img is None:
        return None
    box_filter_size = 11
    bl_img = cv2.blur(bin_img, (box_filter_size, box_filter_size))
    
    # filters should be applied here
    _, t4 = cv2.threshold(bl_img, 15, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_not(t4)
    
    img_for_Hough = cv2.bitwise_and(bin_img, mask)
    lines = None
    thr *= 2
    counter = 0
    while lines is None or lines.size == 0:
        thr /= 2
        lines = cv2.HoughLines(img_for_Hough, rho_step, theta_step, thr)
        counter += 1
        if counter > 5:
            break
    
#     # strongest line
#     rho, theta = lines[0, 0]
#     
#     add_lines_to_image(bin_img, [lines[0]])
    return lines


def Hough_lines_opencv(event, parameters):
    sigmaXY = parameters.get("sigmaXY") or 0.7
    thr = parameters.get("threshold") or 19
    max_n_lines = parameters.get("n_lines_max") or 5
#     print parameters

    mhl = make_me_happy(event, thr=thr)
    if mhl is None:
        return
    n_lines = min([max_n_lines, len(mhl)])
    for l in mhl[0:n_lines]:
        event.adjust_track(l[0], sigmaXY)
    




