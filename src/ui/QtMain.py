from PySide6 import QtCore, QtWidgets

from src.ModelManager import ModelManager
from src.AudioProcessor import AudioProcessor

class MyWidget(QtWidgets.QWidget):
    
    model_name = None
    model_list = None
    model_manager = None

    def __init__(self):
        super().__init__()

        self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_group_box()
        self.textOutputs = QtWidgets.QPlainTextEdit("Output Text Box")
        self.textOutputs.setReadOnly(True)
        self.textStatus = QtWidgets.QLineEdit("Status Bar",
                                     alignment=QtCore.Qt.AlignCenter)
        self.textStatus.setReadOnly(True)
        # self.textStatus.setStyleSheet("background-color: lightgray;")

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
        self.model_list = model_manager.get_model_list()
        self.buttonModelOption = QtWidgets.QComboBox()
        self.buttonModelOption.addItems(self.model_list)
        # buttonModelOption.setMaximumWidth(300)
        layout.addWidget(self.buttonModelOption)
        
        buttonSelectFile = QtWidgets.QPushButton("Select File")
        buttonSelectFile.clicked.connect(self.select_file)
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
        buttonDownload.clicked.connect(self.download_model)
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
        file_path , filterType = QtWidgets.QFileDialog.getOpenFileName(filter='(*.mp3 *.wav *.flac *.ogg *.m4a)')
        self.textStatus.setText("Selected file: " + file_path + " " + filterType)
        
        import time
        time.sleep(1)
        self.textStatus.setText("Trascription in progress...")

        self.model_name = self.buttonModelOption.currentText()
        audio_processor = AudioProcessor()
        audio_data = audio_processor.preprocess_audio(file_path)
        start_time = time.time()
        trascription = audio_processor.transcribeAudio(audio_data, self.model_name)
        end_time = time.time()
        print(trascription)
        self.textOutputs.setPlainText(trascription)
        self.textStatus.setText("Trascription completed.   " + "Time: " + str(end_time - start_time) + "s   " + "Model: " + self.model_name)
        