from PyQt5 import QtCore, QtWidgets

class ParameterView():
    def __init__(self, parentWidget, name, units, default_value=0):
        self.widget = QtWidgets.QWidget(self.parentWidget)
        self.widget.setObjectName("widget")
        self.layout = QtWidgets.QHBoxLayout(self.widget)
        self.layout.setObjectName("layout")
        self.name_label = QtWidgets.QLabel(self.widget)
        self.name_label.setObjectName("name_label")
        self.layout.addWidget(self.name_label)
        self.line_edit = QtWidgets.QLineEdit(self.widget)
        self.line_edit.setMaximumSize(QtCore.QSize(80, 16777215))
        self.line_edit.setObjectName("line_edit")
        self.layout.addWidget(self.line_edit)
        self.units_label = QtWidgets.QLabel(self.widget)
        self.units_label.setObjectName("units_label")
        self.layout.addWidget(self.units_label)
        
    def set_validator(self, validator):
        self.validate = validator
        
    def get_value(self):
        value = self.line_edit.text()
        return self.validate(value)
        
    
        