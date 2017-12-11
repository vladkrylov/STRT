from matplotlib import path
from matplotlib.widgets import Lasso
from matplotlib.collections import RegularPolyCollection
from matplotlib.colors import colorConverter
from numpy import nonzero

class MyLasso(Lasso):
    def onrelease(self, event):
        """Overwrite the default onrelease method for the case when self.line
was deleted before onrelease called"""
        if self.ignore(event):
            return
        if self.verts is not None:
            self.verts.append((event.xdata, event.ydata))
            if len(self.verts) > 2:
                self.callback(self.verts)
            if self.line in self.ax.lines:
                self.ax.lines.remove(self.line)
        self.verts = None
        self.disconnect_events()

class LassoManager(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.dummy_already_pressed = False  # single click bugfix
                                            # see the commit 1eab67 for details
        self.cid = None
        
    def add_listener(self, listener):
        self.listener = listener
        
    def set_points(self, ax, data):  # FIXME unused parameter 'ax' ? 
        self.xys = data
        self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)

    def callback(self, verts):
        p = path.Path(verts)
        self.ind = nonzero([p.contains_point(xy) for xy in self.xys])[0]
        print(self.ind)
        self.canvas.draw_idle()
        self.canvas.widgetlock.release(self.lasso)
        del self.lasso
#         self.lasso.active = False
        # wtf??? #
#         self.canvas.mpl_disconnect(self.cid)
#         self.cid = self.canvas.mpl_connect('button_press_event', self.onpress)
        # ------ #
        self.dummy_already_pressed = False
        self.listener.on_hits_selected(self.ind)

    def onpress(self, event):
        if self.canvas.widgetlock.locked():
            if self.dummy_already_pressed:
                self.canvas.widgetlock.release(self.lasso)
                del self.lasso
            else:
                print("Canvas is locked somehow")
                return
        if event.inaxes is None:
            return
        self.lasso = MyLasso(event.inaxes,
                           (event.xdata, event.ydata),
                           self.callback)
        # acquire a lock on the widget drawing
        self.canvas.widgetlock(self.lasso)
        self.dummy_already_pressed = True
        
    def stop_selection(self):
        if self.cid:
            self.canvas.mpl_disconnect(self.cid)
#         if self.lasso and 
#         self.canvas.widgetlock.release(self.lasso)
        