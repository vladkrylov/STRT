from subprocess import call

def substitute(file_path, str_what, str_by):
    with open(file_path, 'r') as pyform:
        content = pyform.read()
        content = content.replace(str_what, str_by)
    with open(file_path, 'w') as pyform:
        pyform.write(content)


def subs_icons_path(pyform_file):
    substitute(pyform_file, 'addPixmap(QtGui.QPixmap("img/', 'addPixmap(QtGui.QPixmap("view/img/')


def add_matplotlib_widget_import(pyform_file):
    str_to_find = "from PyQt5 import QtCore, QtGui, QtWidgets"
    str_substit = "%s\nfrom axes import PlotCanvas, MatplotlibToolbar" % str_to_find
    substitute(pyform_file, str_to_find, str_substit)


def add_matplotlib_widget(pyform_file):
    substitute(pyform_file, "self.plotWidget = QtWidgets.QWidget(self.centralwidget)", "self.plotWidget = PlotCanvas(self.centralwidget)")


def add_matplotlib_widget_and_toolbar(pyform_file):
    substitute(pyform_file, "self.matplotlibToolbar = QtWidgets.QWidget(self.centralwidget)",
               """self.plotWidget = PlotCanvas(self.centralwidget)
        self.matplotlibToolbar = MatplotlibToolbar(self.plotWidget, self.centralwidget)
        """)
    substitute(pyform_file, "self.plotWidget = QtWidgets.QWidget(self.centralwidget)", "")


def generate_mainwindow():
    qtform_file = "mainwindow.ui"
    pyform_file = "mainwindow.py"
    qt2py_command = "pyuic5 -x %s -o %s" % (qtform_file, pyform_file)
    call(qt2py_command.split())

    add_matplotlib_widget_import(pyform_file)
    subs_icons_path(pyform_file)
    add_matplotlib_widget_and_toolbar(pyform_file)

# FIXME add docstrings, fix dry
def analysis_add_matplotlib_widget_import(pyform_file):
    str_to_find = "from PyQt5 import QtCore, QtGui, QtWidgets"
    str_substit = "%s\nfrom axes import TrackParametersCanvas, HoughTransformCanvas, MatplotlibToolbar" % str_to_find
    substitute(pyform_file, str_to_find, str_substit)


def analysis_add_matplotlib_widget_and_toolbar(pyform_file):
    substitute(pyform_file, "self.parametersMatplotlibToolbar = QtWidgets.QWidget(self.parametersWidgetPage)",
               """self.parametersPlotWidget = TrackParametersCanvas(self.parametersWidgetPage)
        self.parametersMatplotlibToolbar = MatplotlibToolbar(self.parametersPlotWidget, self.parametersWidgetPage)
        """)
    substitute(pyform_file, "self.parametersPlotWidget = QtWidgets.QWidget(self.parametersWidgetPage)", "")


def Hough_add_matplotlib_widget_and_toolbar(pyform_file):
    substitute(pyform_file, "self.HTMatplotlibToolbar = QtWidgets.QWidget(self.HoughWidgetPage)",
               """self.HTCanvas = HoughTransformCanvas(self.HoughWidgetPage)
        self.HTMatplotlibToolbar = MatplotlibToolbar(self.HTCanvas, self.HoughWidgetPage)
        """)
    substitute(pyform_file, "self.HTCanvas = QtWidgets.QWidget(self.HoughWidgetPage)", "")
    

def generate_analysis_form():
    qtform_file = "tracks_parameters.ui"
    pyform_file = "tracks_parameters.py"
    qt2py_command = "pyuic5 -x %s -o %s" % (qtform_file, pyform_file)
    call(qt2py_command.split())
    
    analysis_add_matplotlib_widget_import(pyform_file)
    analysis_add_matplotlib_widget_and_toolbar(pyform_file)
    Hough_add_matplotlib_widget_and_toolbar(pyform_file)

if __name__ == "__main__":
    generate_mainwindow()
    generate_analysis_form()
    

