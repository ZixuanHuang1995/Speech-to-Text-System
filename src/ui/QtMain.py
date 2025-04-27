# from src import config
import sys
from PySide6 import QtCore, QtWidgets, QtMultimedia

from src.ModelManager import ModelManager
from src.AudioProcessor import AudioProcessor
from src.RecordingManager import RecordingManager

class MyWidget(QtWidgets.QWidget):
    
    model_name = None
    language = None
    model_list = None
    model_manager = None
    recording = False

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
        layout.addWidget(self.buttonModelOption)

        self.buttonLanguageOption = QtWidgets.QComboBox()
        self.buttonLanguageOption.addItems(['zh', 'en', 'ja', 'ko'])
        layout.addWidget(self.buttonLanguageOption) 
        
        buttonSelectFile = QtWidgets.QPushButton("Select File")
        buttonSelectFile.clicked.connect(self.select_file)
        layout.addWidget(buttonSelectFile)
        
        
        buttonMicrophone = QtWidgets.QPushButton("Microphone On/Off")
        buttonMicrophone.clicked.connect(self.record_to_transcribe)
        layout.addWidget(buttonMicrophone)

        self._horizontal_group_box.setLayout(layout)
    
    def create_grid_group_box(self):
        self._grid_group_box = QtWidgets.QGroupBox("Advanced Controls")
        layout = QtWidgets.QGridLayout()

        self.checkboxAuto = QtWidgets.QCheckBox("Auto Scroll")
        layout.addWidget(self.checkboxAuto, 1, 0)

        checkboxDetection = QtWidgets.QCheckBox("Detection")
        layout.addWidget(checkboxDetection, 2, 0)
        
        buttonSaveOutputs = QtWidgets.QPushButton("Save File")
        buttonSaveOutputs.clicked.connect(self.save_file)
        layout.addWidget(buttonSaveOutputs, 1, 3)

        buttonDownload = QtWidgets.QPushButton("Download Models")
        buttonDownload.clicked.connect(self.download_model)
        layout.addWidget(buttonDownload, 2, 3)

        layout.setColumnStretch(1, 20)
        layout.setColumnStretch(2, 10)
        self._grid_group_box.setLayout(layout)
    
    @QtCore.Slot()
    def download_model(self):
        model_manager = ModelManager()
        try:
            model_manager.download_model(self.model_list)
            QtWidgets.QMessageBox.warning(None, "Warning", "Models downloaded successfully")
            self.textStatus.setText("All models downloaded successfully.")
        except Exception as e: 
            self.textStatus.setText(f"Error downloading models: {e}")
    
    @QtCore.Slot()
    def save_file(self):
        self.model_name = self.buttonModelOption.currentText()
        self.language = self.buttonLanguageOption.currentText()
        with open('output/output.txt', 'w') as output_file:
            output_file.write(str(self.textOutputs.toPlainText()))
            output_file.write("\n\n" + "Meta data: " + "model_name:" + str(self.model_name) + " language:" + str(self.language) + " timstamp:" + str(QtCore.QDateTime.currentDateTime().toString()))
        self.textStatus.setText("File saved successfully.")
    
    @QtCore.Slot()
    def select_file(self):
        file_path = None
        try:
            file_path , filterType = QtWidgets.QFileDialog.getOpenFileName(filter='(*.mp3 *.wav *.flac *.ogg *.m4a)')
            self.textStatus.setText("Selected file: " + file_path + " " + filterType)
        except Exception as e:
            self.textStatus.setText(f"Error: {e}")
            QtWidgets.QMessageBox.warning(None, "Warning", "Please select a valid audio file.")
            self.textOutputs.setPlainText("")
        
        if file_path:
            self.textStatus.setText("Trascription in progress...")
            import time
            self.model_name = self.buttonModelOption.currentText()
            self.language = self.buttonLanguageOption.currentText()
            audio_processor = AudioProcessor()
            audio_data = audio_processor.preprocess_audio(file_path)
            try:
                start_time = time.time()
                trascription = audio_processor.transcribe_audio(audio_data, self.model_name, self.language)
                end_time = time.time()
            except Exception as e:
                self.textStatus.setText(f"Error: {e}")
                QtWidgets.QMessageBox.warning(None, "Warning", "Please select a valid audio file.")
                self.textOutputs.setPlainText("")
                return

            print(trascription)
            self.textOutputs.setPlainText(trascription)
            self.textStatus.setText("Trascription completed.   " + "Time: " + str(end_time - start_time) + "s   " + "Model: " + self.model_name)
        else:   
            self.textStatus.setText("Please select a valid audio file.")
            self.textOutputs.setPlainText("")

    @QtCore.Slot()
    def record_to_transcribe(self):
        self.model_name = self.buttonModelOption.currentText()
        recording_manager = RecordingManager()
        input_devices = recording_manager.get_input_devices()
        if not input_devices:
            QtWidgets.QMessageBox.warning(None, "audio", "There is no audio input device available.")
            sys.exit(-1)
        input_device = input_devices[1]
        
        self.recording = not self.recording
        if self.recording:
            self.textStatus.setText("Recording...")
            recording_manager.start_recording(input_device, self.model_name)
            recording_manager.transcription_updated.connect(self.append_transcription)
        else:
            recording_manager.stop_recording()
            self.textStatus.setText("Recording stopped.")
    
    def append_transcription(self, text):
        self.textStatus.append('text') 

    def add_text(self, text):
        self.textOutputs.appendPlainText(text)
        self.textOutputs.moveCursor(QtWidgets.QTextCursor.End)
        self.textOutputs.ensureCursorVisible()

        if self.checkboxAuto.isChecked():
            self.textOutputs.verticalScrollBar().setValue(self.textOutputs.verticalScrollBar().maximum())
    