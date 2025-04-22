from PySide6 import QtCore, QtWidgets

from src.ModelManager import ModelManager

class MyWidget(QtWidgets.QWidget):
    
    model_name = None
    model_list = None
    model_manager = None

    def __init__(self):
        super().__init__()

        self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_group_box()
        self.textOutputs = QtWidgets.QLabel("Output Text Box",
                                     alignment=QtCore.Qt.AlignCenter)
        self.textStatus = QtWidgets.QLabel("Status Bar",
                                     alignment=QtCore.Qt.AlignCenter)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setMenuBar(self._menu_bar)
        main_layout.addWidget(self._horizontal_group_box)
        main_layout.addWidget(self._grid_group_box)
        main_layout.addWidget(self.textOutputs)
        main_layout.addWidget(self.textStatus)
        self.setLayout(main_layout)

        self.setWindowTitle("Qt Main Window")

    def create_menu(self):
        self._menu_bar = QtWidgets.QMenuBar()

        self._file_menu = QtWidgets.QMenu("&File", self)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QtWidgets.QGroupBox("Basic Components")
        layout = QtWidgets.QHBoxLayout()
        
        model_manager = ModelManager()
        model_list = model_manager.get_model_list()
        buttonModelOption = QtWidgets.QComboBox()
        buttonModelOption.addItems(model_list)
        print("Model list: ", model_list, "done")
        # buttonModelOption.setMaximumWidth(300)
        layout.addWidget(buttonModelOption)
        
        buttonSelectFile = QtWidgets.QPushButton("Select File")
        layout.addWidget(buttonSelectFile)
        
        buttonMicrophone = QtWidgets.QPushButton("Microphone On/Off")
        layout.addWidget(buttonMicrophone)

        self._horizontal_group_box.setLayout(layout)
    
    def create_grid_group_box(self):
        self._grid_group_box = QtWidgets.QGroupBox("Advanced Controls")
        layout = QtWidgets.QGridLayout()

        checkboxAuto = QtWidgets.QCheckBox("Auto")
        layout.addWidget(checkboxAuto, 1, 0)

        checkboxDetection = QtWidgets.QCheckBox("Detection")
        layout.addWidget(checkboxDetection, 2, 0)
        
        buttonSaveOutputs = QtWidgets.QPushButton("Save File")
        layout.addWidget(buttonSaveOutputs, 1, 1)

        buttonDownload = QtWidgets.QPushButton("Download Models")
        layout.addWidget(buttonDownload, 2, 1)

        layout.setColumnStretch(1, 20)
        layout.setColumnStretch(2, 10)
        self._grid_group_box.setLayout(layout)
    
    @QtCore.Slot()
    def download_model(self):
        model_manager = ModelManager()
        model_manager.download_model(self.model_list)
    
    @QtCore.Slot()
    def select_file(self):
        import os
        