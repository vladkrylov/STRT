# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'runs.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(222, 391)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.RunsTable = QtWidgets.QTableWidget(self.dockWidgetContents)
        self.RunsTable.setObjectName("RunsTable")
        self.gridLayout.addWidget(self.RunsTable, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.AddRunButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.AddRunButton.setObjectName("AddRunButton")
        self.horizontalLayout.addWidget(self.AddRunButton)
        self.RemoveRunButton = QtWidgets.QPushButton(self.dockWidgetContents)
        self.RemoveRunButton.setObjectName("RemoveRunButton")
        self.horizontalLayout.addWidget(self.RemoveRunButton)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "R&uns"))
        self.AddRunButton.setText(_translate("DockWidget", "Add Run"))
        self.RemoveRunButton.setText(_translate("DockWidget", "Remove Run"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DockWidget = QtWidgets.QDockWidget()
    ui = Ui_DockWidget()
    ui.setupUi(DockWidget)
    DockWidget.show()
    sys.exit(app.exec_())

