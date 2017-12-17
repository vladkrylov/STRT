import argparse

from controller import Controller
from model import Model


def console_app(args):
    import os
    
    c = Controller(m, None)
    parameters = {'sigmaXY': 0.6, 'threshold': 1, 'n_lines_max': 5}
    for r in args.runs:
        run_path = os.path.abspath(r)
        if not os.path.exists(run_path):
            continue
        run_name = os.path.basename(run_path)
        run_id = c.on_new_run(run_name)
        
        event_files = [os.path.join(run_path, f) for f in os.listdir(run_path) if f.startswith('Event') and f.endswith('.txt')]
        c.on_load_events(run_id, event_files)
        c.on_reconstruct_all_events(run_id, parameters)
    
    save_path = os.path.abspath(args.out_file)
    c.on_save_session(save_path)


def gui_app():
    import sys
    from PyQt5 import QtWidgets
    from view.qt_gui import QtGui

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = QtGui()
    ui.setupUi(MainWindow)
    
    c = Controller(m, ui)

    MainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Options.')
    parser.add_argument('-r', '--runs', nargs='+', help='Run directories')
    parser.add_argument('-o', '--out_file', help='output ROOT file')

    args = parser.parse_args()
    print args

    m = Model()
    # TODO : correct console app condition is when no arguments were provided
    if args.runs is None:
        # GUI is starting
        gui_app()
    else:
        # console version
        console_app(args)

#     # Tests
#     import unittest
#     from ptests import *
#     suites = []
#     suites.append(unittest.TestLoader().loadTestsFromTestCase(TestControllerModelInterface))
#     suites.append(unittest.TestLoader().loadTestsFromTestCase(TestModelAPI))
#     for suite in suites:
#         unittest.TextTestRunner(verbosity=2).run(suite)
