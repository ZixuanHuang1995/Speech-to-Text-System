import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.buttonModelOption = QtWidgets.QComboBox()
        self.buttonModelOption.addItems(["tiny", "base", "large"])
        self.buttonModelOption.setMaximumWidth(300)
        self.buttonSelectFile = QtWidgets.QPushButton("Select File")
        self.buttonMicrophone = QtWidgets.QPushButton("Microphone On/Off")
        self.buttonSaveOutputs = QtWidgets.QPushButton("Save File")

        self.checkboxAuto = QtWidgets.QCheckBox("Auto")
        self.checkboxDetection = QtWidgets.QCheckBox("Detection")

        self.textOutputs = QtWidgets.QLabel("Output Text Box",
                                     alignment=QtCore.Qt.AlignCenter)
        self.textStatus = QtWidgets.QLabel("Status Bar",
                                     alignment=QtCore.Qt.AlignCenter)
        
        widgets = [self.buttonModelOption, self.buttonSelectFile,
            self.buttonMicrophone, self.buttonSaveOutputs,
            self.checkboxAuto, self.checkboxDetection,
            self.textOutputs, self.textStatus]
        
        # for widget in widgets:
            # widget.setMinimumHeight(40)
            # widget.setMaximumWidth(200)
            # self.layout.addWidget(widget)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.buttonModelOption)
        self.layout.addWidget(self.buttonSelectFile)
        self.layout.addWidget(self.buttonMicrophone)
        self.layout.addWidget(self.buttonSaveOutputs)
        self.layout.addWidget(self.checkboxAuto)
        self.layout.addWidget(self.checkboxDetection)
        self.layout.addWidget(self.textOutputs)
        self.layout.addWidget(self.textStatus)
        self.layout.addStretch()
        
        self.buttonSelectFile.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.textStatus.setText(random.choice(self.hello))

