# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fasthough.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class ParameterView():
    def __init__(self, parentWidget, name, units, default_value=None):
        self.validate = None
        
        self.widget = QtWidgets.QWidget(parentWidget)
        self.widget.setObjectName("widget")
        self.layout = QtWidgets.QHBoxLayout(self.widget)
        self.layout.setObjectName("layout")
        self.name_label = QtWidgets.QLabel(self.widget)
        self.name_label.setObjectName("name_label")
        self.name_label.setText(str(name))
        self.layout.addWidget(self.name_label)
        self.line_edit = QtWidgets.QLineEdit(self.widget)
        self.line_edit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.line_edit.setObjectName("line_edit")
        if default_value is not None:
            self.line_edit.setText(str(default_value))
        self.layout.addWidget(self.line_edit)
        self.units_label = QtWidgets.QLabel(self.widget)
        self.units_label.setObjectName("units_label")
        self.units_label.setText(str(units))
        self.layout.addWidget(self.units_label)
        
    def set_validator(self, validator):
        self.validate = validator
        
    def get_value(self):
        value = self.line_edit.text()
        if self.validate:
            return self.validate(value)
        else:
            return value


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        self.parameters = {}
        
        DockWidget.setObjectName("DockWidget")
        DockWidget.resize(176, 395)
        self.fastHTWidget = QtWidgets.QWidget()
        self.fastHTWidget.setObjectName("fastHTWidget")
        self.layout = QtWidgets.QVBoxLayout(self.fastHTWidget)
        self.layout.setObjectName("layout")

        self.widget = QtWidgets.QWidget(self.fastHTWidget)
        self.widget.setObjectName("widget")
#         self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
#         self.horizontalLayout_2.setObjectName("horizontalLayout_2")
#         self.label = QtWidgets.QLabel(self.widget)
#         self.label.setObjectName("label")
#         self.horizontalLayout_2.addWidget(self.label)
#         self.lineEdit = QtWidgets.QLineEdit(self.widget)
#         self.lineEdit.setMaximumSize(QtCore.QSize(80, 16777215))
#         self.lineEdit.setObjectName("lineEdit")
#         self.horizontalLayout_2.addWidget(self.lineEdit)
#         self.label_2 = QtWidgets.QLabel(self.widget)
#         self.label_2.setObjectName("label_2")
#         self.horizontalLayout_2.addWidget(self.label_2)
#         self.layout.addWidget(self.widget)
        
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.layout.addItem(spacerItem)
        
        self.reconstructAllButton = QtWidgets.QPushButton(self.fastHTWidget)
        self.reconstructAllButton.setObjectName("reconstructAllButton")
        self.reconstructAllButton.setText("Reconstruct all events")
        self.layout.addWidget(self.reconstructAllButton)
        
        self.findLinesButton = QtWidgets.QPushButton(self.fastHTWidget)
        self.findLinesButton.setObjectName("findLinesButton")
        self.layout.addWidget(self.findLinesButton)
        
        DockWidget.setWidget(self.fastHTWidget)

        self.retranslateUi(DockWidget)
        QtCore.QMetaObject.connectSlotsByName(DockWidget)

    def retranslateUi(self, DockWidget):
        _translate = QtCore.QCoreApplication.translate
        DockWidget.setWindowTitle(_translate("DockWidget", "Para&meters"))
        self.findLinesButton.setText(_translate("DockWidget", "Find tracks"))
#         self.label.setText(_translate("DockWidget", "parName"))
#         self.label_2.setText(_translate("DockWidget", "units"))
        
    def add_parameter(self, name, units, validator, default_value=None):
        pv = ParameterView(self.fastHTWidget, name, units, default_value)
        pv.set_validator(validator)
        n_items = self.layout.count()
        position = n_items - 3  # append before button and spacer
        self.layout.insertWidget(position, pv.widget)
        self.parameters[name] = pv
        
    def get_params(self):
        return {name: pv.get_value() for name, pv in self.parameters.iteritems()}
    
