import numpy as np

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIntValidator
from mainwindow import Ui_MainWindow
from view.qt_track_representation import TrackRepresentation
from lasso_manager import LassoManager
from tracks_parameters import Ui_DockWidget as analysis_form
from fasthough import Ui_DockWidget as fastHT_form
from runs_table import Ui_DockWidget as runs_table_form
from matplotlib.backends.backend_pdf import PdfPages

class QtGui(Ui_MainWindow):
    def __init__(self):
        super(QtGui, self).__init__()
        self.run_ids = []
        self.current_run = None
        self.current_event = None
        self.tracks = []
        self.Houghlines = []
        self.hits_selection_is_on = None
        self.current_events_cache = {}  # run_id: current_event_id
        
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        self.tracksLayout = self.verticalLayout_6
        self.lasso = LassoManager(self.plotWidget.figure.canvas)
        self.lasso.add_listener(self)
        # analysis form
        self.analysis_widget = QtWidgets.QDockWidget(MainWindow)
        self.analysis_form = analysis_form()
        self.analysis_form.setupUi(self.analysis_widget)
        MainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.analysis_widget)
        self.analysis_widget.hide()
        #
        self.runs_table_widget = QtWidgets.QDockWidget(MainWindow)
        self.runs_table_widget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.runs_table_form = runs_table_form()
        self.runs_table_form.setupUi(self.runs_table_widget)
        self.prepare_runs_table()
        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.runs_table_widget)
        # 
        self.fastHT_widget = QtWidgets.QDockWidget(MainWindow)
        self.runs_table_widget.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Expanding)
        self.fastHT_form = fastHT_form()
        self.fastHT_form.setupUi(self.fastHT_widget)
        MainWindow.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.fastHT_widget)
        self.fastHT_form.add_parameter("threshold", "", lambda x: int(x), 1)
        self.fastHT_form.add_parameter("sigmaXY", "mm", lambda x: float(x), 0.6)
        self.fastHT_form.add_parameter("n_lines_max", "", lambda x: int(x), 5)
        self.fastHT_form.add_parameter("gap_length", "mm", lambda x: float(x), 2.)
        self.fastHT_form.add_parameter("nbins_dEdx", "", lambda x: int(x), 100)
        
        # css
        self.connect_signals_slots()
        
    def connect_signals_slots(self):
        # matplotlib events
        self.plotWidget.mpl_connect('pick_event', self.on_pick)
        # Qt toolbar actions
        self.action_load_event.triggered.connect(self.load_new_event)
        self.action_previous_event.triggered.connect(self.prev_event)
        self.action_next_event.triggered.connect(self.next_event)
        self.action_select_new_track.triggered.connect(self.add_new_track)
        self.action_add_hits_to_track.triggered.connect(self.add_hits)
        self.action_remove_hits.triggered.connect(self.remove_hits)
        self.action_save_PDF.triggered.connect(self.save_pdf)
        self.action_save_all_PDF.triggered.connect(self.save_all_pdf)
        self.action_good_track.triggered.connect(self.good_track)
        self.action_bad_track.triggered.connect(self.bad_track)
        self.action_export_to_matlab.triggered.connect(self.export_to_matlab)
        self.action_plot_dE_dx.triggered.connect(self.plot_dEdx)
        # Qt menu actions
        self.action_save_session.triggered.connect(self.save_session)
        self.action_load_session.triggered.connect(self.load_session)
        self.action_Hough_transform.triggered.connect(self.show_Hough_transform_canvas)
        self.action_explore_parameters.triggered.connect(self.explore_parameters)
        # 
        self.analysis_form.transfomEventButton.clicked.connect(self.event_Hough_transform_requested)
        self.analysis_form.transformTrackButton.clicked.connect(self.track_Hough_transform_requested)
        #
        self.fastHT_form.reconstructAllButton.clicked.connect(self.reconstruct_all)
        self.fastHT_form.findLinesButton.clicked.connect(self.fast_Hough_lines)
        #
        self.runs_table_form.AddRunButton.clicked.connect(self.add_run)
        self.runs_table_form.RemoveRunButton.clicked.connect(self.remove_run)
        self.runs_table_form.RunsTable.cellChanged.connect(self.run_name_changed)
        self.runs_table_form.RunsTable.currentCellChanged.connect(self.new_run_selected)
    
    def message_to_user(self, mtype, text1, text2=None, text3=None):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(mtype)
        msg.setText(text1)
        if text2:
            msg.setInformativeText(text2)
#         msg.setWindowTitle("MessageBox demo")
        if text3:
            msg.setDetailedText(text3)
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
        
    def info_message(self, text1, text2=None, text3=None):
        self.message_to_user(QtWidgets.QMessageBox.Information, text1, text2, text3)
    
    def error_message(self, text1, text2=None, text3=None):
        self.message_to_user(QtWidgets.QMessageBox.Error, text1, text2, text3)
        
    def add_listener(self, controller):
        self.controller = controller
        # track parameters list initialization
        self.track_parameters = sorted(self.controller.get_track_parameters())
        self.trackParamsRadioButtons = []
        for p in self.track_parameters:
            self.trackParamsRadioButtons.append(QtWidgets.QRadioButton(self.analysis_form.parameterNames))
            self.trackParamsRadioButtons[-1].setObjectName("%sRadioButton" % p)
            self.trackParamsRadioButtons[-1].setText(p)
            self.analysis_form.verticalLayout.addWidget(self.trackParamsRadioButtons[-1])
        self.trackParamsRadioButtons[0].setChecked(True)
        for rb in self.trackParamsRadioButtons:
            rb.toggled.connect(self.track_param_changed)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.analysis_form.verticalLayout.addItem(spacerItem)
        self.computeParametersButton = QtWidgets.QPushButton(self.analysis_form.parameterNames)
        self.computeParametersButton.setObjectName("computeParametersButton")
        self.computeParametersButton.setText("Recalculate")
        self.analysis_form.verticalLayout.addWidget(self.computeParametersButton)
        self.computeParametersButton.clicked.connect(self.recalculate_track_parameters)
        # finish track parameters list initialization
        self.add_binning_toolbar()
    
    def load_new_event(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        test_file_path = "indata/Run25"
        filenames = QtWidgets.QFileDialog.getOpenFileNames(self.centralwidget, "QFileDialog.getOpenFileNames()", test_file_path, "All Files (*)")
        self.controller.on_load_events(run_id, filenames[0])
    
    def update_with_event(self, event, is_first=False, is_last=False):
        if event is None:
            self.plotWidget.clear()
            return
        run_id = self.get_selected_run_id(error_dialog=True)
        self.current_event = event
        self.current_events_cache[run_id] = event.id
        points = [(h.x, h.y) for h in event.hits]
        x = map(lambda point: point[0], points)
        y = map(lambda point: point[1], points)
        self.plotWidget.plot(x, y)
        self.handle_events_navigation(is_first, is_last)
        self.update_status_bar(event)
        self.update_track_list(event)
        print "Canvas successfully updated"
        print event
#         print event.tracks
        
    def update_track_list(self, event):
        self.clear_track_list()
        for track in event.tracks:
            x = map(lambda ihit: event.hits[ihit].x, track.hit_indices)
            y = map(lambda ihit: event.hits[ihit].y, track.hit_indices)
#             self.plotWidget.add_track_hits(x, y, track.color)
            
            t = TrackRepresentation(track, self.scrollAreaWidgetContents, self.tracksLayout, self.plotWidget)
            self.tracks.append(t)
            if t.track.displayed:
                t.show_line(x, y)
                t.check_box.setChecked(True)  # TODO check if slot is called here
            else:
                t.hide_line()
                t.check_box.setChecked(False)
        
    def clear_track_list(self):
        n = 0
        while len(self.tracks) != 0:
#             self.tracks.pop()
            del(self.tracks[0])
            
        while self.tracksLayout.count() > n:
            x = self.tracksLayout.itemAt(n)
            if x.widget():
                x.widget().setParent(None)
            else:
                n += 1
    
    def handle_events_navigation(self, is_first, is_last):
        if is_first and is_last:
            self.action_previous_event.setEnabled(False)
            self.action_next_event.setEnabled(False)
        elif is_first:
            self.action_previous_event.setEnabled(False)
            self.action_next_event.setEnabled(True)
        elif is_last:
            self.action_previous_event.setEnabled(True)
            self.action_next_event.setEnabled(False)
        else:
            self.action_next_event.setEnabled(True)
            self.action_previous_event.setEnabled(True)
    
    def update_status_bar(self, event):
        self.statusBar.showMessage(str(event))
    
    def prev_event(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        if self.current_event is None:
            return
        self.controller.on_show_previous_event(run_id, self.current_event)
    
    def next_event(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        if self.current_event is None:
            return
        self.controller.on_show_next_event(run_id, self.current_event)
    
    def add_new_track(self):
        if self.current_event is None:
            return
        self.controller.on_add_track(self.current_event.id)
    
    def remove_track(self):
        if self.current_event is None:
            return
        self.controller.on_remove_track(0)
        
    def on_pick(self, mouse_event):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        if len(self.tracks) == 0:
            return
        if mouse_event.artist not in [t.line for t in self.tracks]:
            # some another artist is selected, not track
            return
        
        for t in self.tracks:
            if t.line == mouse_event.artist and not t.is_selected:
                # t was not selected before, but now it is picked
                t.select()
                self.controller.on_dump_track(run_id, self.current_event.id, t.track.id)
            elif t.line == mouse_event.artist and t.is_selected:
                # t was selected before and now it is picked again, do nothing with it
                pass
            elif t.line != mouse_event.artist and t.is_selected:
                # t was selected before, but now some another track is picked
                t.deselect()
            elif t.line != mouse_event.artist and not t.is_selected:
                # t neither was selected before nor picked now, do nothing with it
                pass
                    
    def add_hits(self):
        if self.action_add_hits_to_track.isChecked():
            if self.action_remove_hits.isChecked():
                self.action_remove_hits.setChecked(False)
            self.select_hits()
        else:
            self.lasso.stop_selection()
    
    def remove_hits(self):
        if self.action_remove_hits.isChecked():
            if self.action_add_hits_to_track.isChecked():
                self.action_add_hits_to_track.setChecked(False)
            self.select_hits()
        else:
            self.lasso.stop_selection()
        
    def select_hits(self):
        print 0
        if self.current_event is None:
            print 1
            return
        t = self.get_selected_track()
        if not t:
            print 2
            return
        print 3
        self.hits_selection_is_on = True
        print 4
        points = [(h.x, h.y) for h in self.current_event.hits]
        print 5
        self.lasso.set_points(self.plotWidget.axes, points)
    
    def get_selected_track(self):
        tracks = [t for t in self.tracks if t.is_selected]
        if len(tracks) != 0:
            return tracks[0]
        return None
    
    def on_hits_selected(self, indices):
        if self.current_event is None:
            return
        t = self.get_selected_track()
        if not t:
            return
        event_id = self.current_event.id
        track_id = t.track.id
        if self.action_add_hits_to_track.isChecked():
            self.controller.on_add_hits(event_id, track_id, indices)
        elif self.action_remove_hits.isChecked():
            self.controller.on_remove_hits(event_id, track_id, indices)
        
    def save_session(self):
#         test_dir_path = "/home/vlad/Program_Files/ilcsoft/marlintpc/workspace/STRT/outdata/Run25"
#         dirname = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, "Open Directory", test_dir_path, QtWidgets.QFileDialog.ShowDirsOnly ) 
#         self.controller.on_save_session(dirname)
#         out_file = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget)
        out_file = 'outdata/test.root'
        self.controller.on_save_session(out_file)
        
    def load_session(self):
#         test_dir_path = "/home/vlad/Program_Files/ilcsoft/marlintpc/workspace/STRT/outdata/Run25"
        test_in_file = 'outdata/test.root'
        in_file = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open Directory", test_in_file) 
        self.controller.on_load_session(in_file[0])
        
    def show_Hough_transform_canvas(self):
        self.analysis_widget.show()
    
    def explore_parameters(self):
        self.analysis_widget.show()
        
    def recalculate_track_parameters(self):
        self.controller.on_recalculate_track_parameters()
        self.track_param_changed()

    def get_chosen_track_parameter(self):
        if not self.track_parameters:
            return None
        n_widgets = self.analysis_form.verticalLayout.count()
        for i in range(n_widgets):
            w = self.analysis_form.verticalLayout.itemAt(i).widget()
            if isinstance(w, QtWidgets.QRadioButton) and w.isChecked():
                p = w.text()
                p = str(p.replace("&", ""))
                if p in self.track_parameters:
                    return p
        return None
    
    def add_binning_toolbar(self):
        # 1) spacer to separate matplotlib items from custom ones
        self.emptyWidget = QtWidgets.QWidget(self.analysis_form.parametersMatplotlibToolbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.emptyWidget.sizePolicy().hasHeightForWidth())
        self.emptyWidget.setSizePolicy(sizePolicy)
        self.emptyWidget.setMinimumSize(QtCore.QSize(10, 0))
        self.emptyWidget.setMaximumSize(QtCore.QSize(10, 16777215))
        self.analysis_form.parametersMatplotlibToolbar.addWidget(self.emptyWidget)
        # 2) label
        self.trackParamBinningLabel = QtWidgets.QLabel(self.analysis_form.parametersMatplotlibToolbar)
        self.trackParamBinningLabel.setObjectName("trackParamBinningLabel")
        self.trackParamBinningLabel.setText("Binning")
        self.analysis_form.parametersMatplotlibToolbar.addWidget(self.trackParamBinningLabel)
        # 3) LineEdit
        self.trackParamBinningLine = QtWidgets.QLineEdit(self.analysis_form.parametersMatplotlibToolbar)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trackParamBinningLine.sizePolicy().hasHeightForWidth())
        self.trackParamBinningLine.setSizePolicy(sizePolicy)
        self.trackParamBinningLine.setMinimumSize(QtCore.QSize(60, 0))
        self.trackParamBinningLine.setMaximumSize(QtCore.QSize(60, 16777215))
        self.trackParamBinningLine.setObjectName("trackParamBinningLine")
        self.analysis_form.parametersMatplotlibToolbar.addWidget(self.trackParamBinningLine)
        # 4) slider
        self.trackParamBinningSlider = QtWidgets.QSlider(self.analysis_form.parametersMatplotlibToolbar)
        self.trackParamBinningSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.trackParamBinningSlider.setOrientation(QtCore.Qt.Horizontal)
        self.trackParamBinningSlider.setObjectName("trackParamBinningSlider")
        self.analysis_form.parametersMatplotlibToolbar.addWidget(self.trackParamBinningSlider)
        # 5) synchronize lineedit and slider
        self.sync_nbins_lineedit_slider()
        self.add_tooltip_to_slider(self.trackParamBinningSlider)
        
    def add_tooltip_to_slider(self, sliderWidget):
        sliderWidget.valueChanged.connect(self.track_param_slider_val_changed)
    
    def track_param_slider_val_changed(self, value):
        # taken from here https://stackoverflow.com/questions/31653647/how-to-make-a-tip-to-follow-the-handler-of-slider-with-pyqt
        slider = self.trackParamBinningSlider
        style = slider.style()
        opt = QtWidgets.QStyleOptionSlider()
        slider.initStyleOption(opt)
        rect_handle = style.subControlRect(QtWidgets.QStyle.CC_Slider, opt, QtWidgets.QStyle.SC_SliderHandle, self.analysis_form.parametersMatplotlibToolbar)
        tip_offset = QtCore.QPoint(0, -45)
        pos_local = rect_handle.topLeft() + tip_offset
        pos_global = slider.mapToGlobal(pos_local)
        QtWidgets.QToolTip.showText(pos_global, str(value), slider)
        
    def sync_nbins_lineedit_slider(self):
        self.trackParamBinningLine.returnPressed.connect(self.track_param_lineedit2slider)
        self.trackParamBinningSlider.sliderReleased.connect(self.track_param_slider2lineedit)
        
    def track_param_lineedit2slider(self):
        val = int(self.trackParamBinningLine.text())
        self.trackParamBinningSlider.setValue(val)
        self.set_nbins_in_hist_track_param(val)
        
    def track_param_slider2lineedit(self):
        val = self.trackParamBinningSlider.value()
        self.trackParamBinningLine.setText(str(val))
        self.set_nbins_in_hist_track_param(val)
        
    def update_nbins_slider_lineedit_range(self, minval, maxval):
        self.trackParamBinningLine.setValidator(QIntValidator(minval, maxval))
        self.trackParamBinningSlider.setRange(minval, maxval)
        
    def set_nbins_track_param(self, n_bins):
        self.n_bins_track_param = n_bins
        self.trackParamBinningLine.setText(str(self.n_bins_track_param))
        self.trackParamBinningSlider.setValue(self.n_bins_track_param)
        
    def set_nbins_in_hist_track_param(self, n_bins):
        self.update_track_param_plot(self.track_param_dist, n_bins)
    
    def update_track_param_plot(self, distribution, n_bins=10):
        # filter None values
        self.track_param_dist = filter(lambda x: x is not None, distribution)
        n_entries = len(self.track_param_dist)
        self.update_nbins_slider_lineedit_range(1, 2*n_entries)
#         if not hasattr(self, "n_bins_track_param") or self.n_bins_track_param > n_entries:
        self.set_nbins_track_param(n_bins)
        # plot 
        axes = self.analysis_form.parametersPlotWidget.axes
        if n_entries == 0:
            axes.clear()
            self.analysis_form.parametersPlotWidget.draw()
            return
        counts, bins, _ = axes.hist(self.track_param_dist, self.n_bins_track_param, linewidth=2, histtype='step', stacked=True, fill=False)
        dy = max(counts)*0.05
        axes.set_ylim([-dy, max(counts)+dy])
#         print "n, bins = ", n, bins
        self.analysis_form.parametersPlotWidget.draw()
        
    def track_param_changed(self):
        chosen_param_name = self.get_chosen_track_parameter()
        self.controller.on_track_param_plot_update(chosen_param_name)
    
    def event_Hough_transform_requested(self):
        self.controller.on_event_Hough_transform(self.current_event.id)
        
    def track_Hough_transform_requested(self):
        current_track_repr = self.get_selected_track()
        if current_track_repr is None:
            return
        self.controller.on_track_Hough_transform(self.current_event.id, self.get_selected_track().track.id)
        
    def update_Hough_transform_canvas(self, HT, lines):
        self.analysis_form.HTCanvas.display_Hough_transform(HT)
        self.display_Houghlines(lines)
        
    def display_Houghlines(self, lines):
        self.clear_Houghlines()
        if len(lines) == 0:
            return
        xmin, xmax = self.plotWidget.axes.get_xlim()
        for l in lines:
            rho, theta = l[0]
            x1 = xmin
            x2 = xmax
            y1 = rho + x1*np.tan(theta)
            y2 = rho + x2*np.tan(theta)
            line = self.plotWidget.add_line((x1, x2), (y1, y2), "k")
            self.Houghlines.append(line)
    
    def clear_Houghlines(self):
        if len(self.Houghlines) != 0:
            for l in self.Houghlines:
                l.set_visible(False)
            self.Houghlines = []

    def fast_Hough_lines(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        parameters = self.fastHT_form.get_params()
        self.controller.on_event_fast_Hough_transform(run_id, self.current_event.id, parameters)

    def reconstruct_all(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        parameters = self.fastHT_form.get_params()
        self.controller.on_reconstruct_all_events(run_id, parameters)

    def save_pdf(self):
        fname = 'STRT_Event%d.pdf' % self.current_event.id
        with PdfPages(fname) as pdf:
            pdf.savefig(self.plotWidget.figure)
            print "%s was created." % fname

    def save_all_pdf(self):
        self.controller.on_save_all_pdf()

    def good_track(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        selected = [t for t in self.tracks if t.is_selected]
        if len(selected) > 0:
            selected[0].hits.set_marker('^')
            self.plotWidget.draw()
            track_id = selected[0].track.id
            self.controller.mark_good_track(run_id, self.current_event.id, track_id, is_good=True)

    def bad_track(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        selected = [t for t in self.tracks if t.is_selected]
        if len(selected) > 0:
            selected[0].hits.set_marker('o')
            self.plotWidget.draw()
            track_id = selected[0].track.id
            self.controller.mark_good_track(run_id, self.current_event.id, track_id, is_good=False)
        
    def export_to_matlab(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        self.controller.export_to_matlab(run_id)

    def plot_dEdx(self):
        run_id = self.get_selected_run_id()
        if run_id is None:
            return
        parameters = self.fastHT_form.get_params()
        gap = parameters.get('gap_length')
        nbins = parameters.get('nbins_dEdx')
        self.controller.on_plot_dEdx(run_id, gap, nbins)
        
    def prepare_runs_table(self):
        t = self.runs_table_form.RunsTable
        t.setRowCount(0)
        t.setColumnCount(1)
        t.horizontalHeader().setStretchLastSection(True)
        t.setHorizontalHeaderLabels(["Run title"])

    def add_run(self):
        t = self.runs_table_form.RunsTable
        run_name = 'New run %d' % (t.rowCount() + 1)
        run_name = run_name.replace(' ', '_')
        self.controller.on_new_run(run_name)
#         t = self.runs_table_form.RunsTable
#         row = t.rowCount() + 1
#         newItem = QtWidgets.QTableWidgetItem('New run %d' % row)
#         t.setRowCount(row)
#         t.setItem(row-1, 0, newItem)
        
    def remove_run(self):
        run_id = self.get_selected_run_id()
        self.controller.on_remove_run(run_id)
        
    def update_run_table(self, runs):
        t = self.runs_table_form.RunsTable
        n_runs = len(runs)
        t.setRowCount(n_runs)
        for i in range(n_runs):
            newItem = QtWidgets.QTableWidgetItem(runs[i].name)
            t.setItem(i, 0, newItem)
        self.run_ids = [run.id for run in runs]
        print [run.name for run in runs]
        
    def get_selected_run_index(self, error_dialog=True):
        '''Returns a index of selected run in the runs table'''
        t = self.runs_table_form.RunsTable
        selected_runs = [index.row() for index in t.selectedIndexes()]
        if len(selected_runs) == 0:
            if error_dialog:
                self.info_message('Please, select a Run from the table to assign the events.')
            return None
        return selected_runs[0]
    
    def get_selected_run_id(self, error_dialog=True):
        '''Returns an id of selected run'''
        run_index = self.get_selected_run_index(error_dialog=error_dialog)
        if run_index is None:
            return None
        return self.run_ids[run_index]
            
    def run_name_changed(self):
        run_index = self.get_selected_run_index(error_dialog=False)
        if run_index is None:
            return
        t = self.runs_table_form.RunsTable
        run_id = self.run_ids[run_index]
        new_name = t.item(run_index, 0).text()
        self.controller.on_run_name_changed(run_id, new_name)
        
    def new_run_selected(self, currentRow, currentColumn, previousRow, previousColumn):
        run_index = currentRow
        run_id = self.run_ids[run_index]
        event_id = self.current_events_cache.get(run_id)
        self.controller.show_event(run_id, event_id)

        



