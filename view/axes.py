import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')

from PyQt5 import QtWidgets
from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from random import uniform

# def set_main_plot_widget(qt_ui):
class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        
#         fig, ax = plt.subplots()
        
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        
        a, b = self.axes.margins()

#         self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
    
    def test_plot(self):
        pass


class PlotCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        
        # customize axes view
        self.axes.xaxis.set_visible(False)
        self.axes.yaxis.set_visible(False)
        self.figure.tight_layout()
        self.figure.subplots_adjust(left=0.00,
                                    right=1.00,
                                    top=1.00,
                                    bottom=0.00)
        self.figure.canvas.draw()

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        
    def test_plot(self, k):
        t = arange(0.0, 3.0, 0.01)
        s = sin(k*pi*t)
        self.axes.plot(t, s)
        self.draw()
        
    def plot(self, x, y, *args):
        if len(x) == 0 or len(x) != len(y):
            return
        self.axes.plot(x, y, 'k.')
        # adjust the ranges
        self.axes.set_xlim([min(x), max(x)])
        self.axes.set_ylim([min(y), max(y)])
        self.draw()
        
    def add_track_line(self, track, xhits, yhits):
        x, y = track.line
        self.axes.hold(True)
        line, = self.axes.plot(x, y, color=track.color)
        line.set_visible(True)
        if track.is_good:
            marker = '^'
        else:
            marker = 'o'
        hits, = self.axes.plot(xhits, yhits, marker, color=track.color)
        hits.set_visible(True)
        self.axes.hold(False)
        self.draw()
        return line, hits
    
    def add_line(self, x, y, color):
        self.axes.hold(True)
        line, = self.axes.plot(x, y, color=color)
        line.set_visible(True)
        self.axes.hold(False)
        self.draw()
        return line
    
    def add_track_hits(self, x, y, color):
        self.axes.hold(True)
        line, = self.axes.plot(x, y, 'o', color=color)
        line.set_visible(True)
        self.axes.hold(False)
        self.draw()
        return line

class TrackParametersCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # customize axes view
        self.figure.tight_layout()
#         self.figure.subplots_adjust(left=0.05,
#                                     right=0.95,
#                                     top=0.98,
#                                     bottom=0.05)
#         self.compute_initial_figure()
        self.figure.canvas.draw()
        
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        
    def test_plot(self, k):
        t = arange(0.0, 3.0, 0.01)
        s = sin(k*pi*t)
        self.axes.plot(t, s)
        self.draw()
        

class HoughTransformCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        # customize axes view
        self.figure.tight_layout()
        self.figure.canvas.draw()
        
    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)
        
    def display_Hough_transform(self, HT):
        img = self.axes.imshow(HT, interpolation='nearest', aspect='auto')
        self.figure.subplots_adjust(left=0.01,
                                    right=0.99,
                                    top=0.99,
                                    bottom=0.01)
        img.set_cmap('hot')
        self.axes.axis('off')
        self.figure.canvas.draw()

        
class MatplotlibToolbar(NavigationToolbar):
    pass


        