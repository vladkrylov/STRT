from PyQt5 import QtWidgets
from view.qt_gui import QtGui
from controller import Controller
from model import Model

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = QtGui()
    ui.setupUi(MainWindow)
    m = Model()
    c = Controller(m, ui)
    
    MainWindow.show()
    sys.exit(app.exec_())

#     # Tests
#     import unittest
#     from ptests import *
#     suites = []
#     suites.append(unittest.TestLoader().loadTestsFromTestCase(TestControllerModelInterface))
#     suites.append(unittest.TestLoader().loadTestsFromTestCase(TestModelAPI))
#     for suite in suites:
#         unittest.TextTestRunner(verbosity=2).run(suite)
