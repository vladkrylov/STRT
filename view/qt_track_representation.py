from PyQt5 import QtCore, QtWidgets

# global constants
MPL_LEFT_BUTTON = 1
MPL_RIGHT_BUTTON = 3

class TrackRepresentation(QtWidgets.QWidget):
    def __init__(self, track, parent_widget, parent_group_box_layout, canvas):
        super(TrackRepresentation, self).__init__(parent_widget)
        self.track = track
        self.canvas = canvas
        self.line = None
        self.hits = None
        self.endpoints = None
        self.cid_point_pick = None
        self.cid_point_move = None
        self.cid_point_release = None
        self.is_selected = None
#         self.im_selected = QtCore.pyqtSignal()
        
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 30))
        self.setObjectName("track%dWidget" % self.track.id)
        self.layout = QtWidgets.QHBoxLayout(self)
        self.layout.setObjectName("track%dLayout" % self.track.id)
        
        self.check_box = QtWidgets.QCheckBox(self)
        self.check_box.setObjectName("track%dCheckBox" % self.track.id)
        self.check_box.setText("Track %d" % self.track.id)
        self.check_box.setChecked(True)
        self.layout.addWidget(self.check_box)
        
        self.colorLabel = QtWidgets.QLabel(self)
        self.colorLabel.setStyleSheet("QLabel {color : %s;}" % self.track.color)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorLabel.sizePolicy().hasHeightForWidth())
        self.colorLabel.setSizePolicy(sizePolicy)
        self.colorLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.colorLabel.setObjectName("track%dColorLabel" % self.track.id)
        self.colorLabel.setText("o")
        self.layout.addWidget(self.colorLabel)
        
        parent_group_box_layout.insertWidget(parent_group_box_layout.count() - 1, self)
        
        self.connect_signals_slots()
        
    def connect_signals_slots(self):
#         self.canvas.mpl_connect('pick_event', self.onpick)
        self.check_box.stateChanged.connect(self.checked)
    
    def show_line(self, xhits, yhits):
        self.track.displayed = True
        track_changed = False
        if not self.track.has_line():
            self.track.set_random_line(self.canvas.axes.get_xlim(), self.canvas.axes.get_ylim())
            track_changed = True
            self.line, self.hits = self.canvas.add_track_line(self.track, xhits, yhits)
        elif self.line is None:
            self.line, self.hits = self.canvas.add_track_line(self.track, xhits, yhits)
        self.line.set_picker(5)  # possibly wrong, should be called when the line is created, not visibility changed
        self.line.set_visible(True)
        self.canvas.draw()
        return track_changed
    
    def hide_line(self):
        self.track.displayed = False
        if self.hits:
            self.hits.set_visible(False)
        if self.line:
            self.line.set_visible(False)
            self.deselect()
            self.canvas.draw()
    
    def checked(self, new_state):
        if new_state == QtCore.Qt.Checked:
            self.track.displayed = True
            if self.hits:
                self.hits.set_visible(True)
            if self.line:
                self.line.set_visible(True)
            self.canvas.draw()
        else:
            self.hide_line()
    
    # TODO: get rid of click_event in the arguments
    def connect_dragndrop(self, click_event):
        print("=== From track %d: %s was picked ===" % (self.track.id, click_event.artist))
        print "event.artist = %s" % str(click_event.artist)
        print "self.line = %s" % str(self.line)
        print "self.endpoints = "
        if self.endpoints is not None:
            for p in self.endpoints:
                print("    %s") % str(p)
        print("=================\n")
        self.select()
        
        mouse_button = click_event.mouseevent.button
        if mouse_button == MPL_LEFT_BUTTON:
            pass
        elif mouse_button == MPL_RIGHT_BUTTON:
            pass
        return
    
    def select(self):
        self.is_selected = True
        self.show_draggable_endpoints()
        
    def deselect(self):
        self.is_selected = False
        self.hide_draggable_endpoints()
        self.cid_point_pick = self.disconnect_mpl_event(self.cid_point_pick)
        
    def show_draggable_endpoints(self):
        if not self.cid_point_pick:
            self.cid_point_pick = self.canvas.mpl_connect('pick_event', self.on_point_pick)
        if self.endpoints is None:
            x, y = self.track.line
            self.canvas.axes.hold(True)
            self.endpoints = [self.canvas.axes.plot(x[i], y[i], 'o', picker=5)[0] for i in range(len(x))]
            self.canvas.axes.hold(False)
        for p in self.endpoints:
            p.set_visible(True)
        self.canvas.draw()
        
    def hide_draggable_endpoints(self):
        if self.endpoints is not None:
            for p in self.endpoints:
                p.set_visible(False)
            self.canvas.draw()
        
    def on_point_pick(self, mouse_event):
        print "=== TR Pick ==="
        print mouse_event.artist
        if not self.is_selected:
            return
        if mouse_event.artist not in self.endpoints:
            return
        self.im_moving = mouse_event.artist
        # multiple calls here, don't know why
        # set None flags to avoid many connection on point pick
        # TODO fix this!
        if self.cid_point_release is None:
            self.cid_point_release = self.canvas.mpl_connect('button_release_event', self.on_point_release)
        if self.cid_point_move is None:
            self.cid_point_move = self.canvas.mpl_connect('motion_notify_event', self.on_point_drag)
        self.select()
        
    def on_point_drag(self, mouse_event):
        if self.im_moving is None:
            return
        print("=== dragging ===")
        print("Moving object is %s" % str(self.im_moving))
        x, y = mouse_event.xdata, mouse_event.ydata
        self.im_moving.set_data(x, y)
        self.show_draggable_endpoints()
        self.update_line_with_endpoints()
        self.update_track()
        
    def update_line_with_endpoints(self):
        xs = [p.get_data()[0] for p in self.endpoints]
        ys = [p.get_data()[1] for p in self.endpoints]
        self.line.set_data(xs, ys)
        self.canvas.draw()
        
    def on_point_release(self, mouse_event):
        self.im_moving = None
        # TODO as well, fix None flags
        self.cid_point_move = self.disconnect_mpl_event(self.cid_point_move)
        self.cid_point_release = self.disconnect_mpl_event(self.cid_point_release)
        self.select()
        
    def update_track(self):
        xs = [p.get_data()[0] for p in self.endpoints]
        ys = [p.get_data()[1] for p in self.endpoints]
        self.track.set_line(xs, ys)
        
    def disconnect_mpl_event(self, mpl_event_id):
        """Disconnect with the flag toggling to prevent connecting many times"""
        self.canvas.mpl_disconnect(mpl_event_id)
        mpl_event_id = None
        return mpl_event_id


