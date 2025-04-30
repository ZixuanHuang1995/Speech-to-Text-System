from PySide6 import QtCore, QtWidgets, QtMultimedia
from PySide6.QtGui import QTextCursor
from datetime import datetime


from src.ModelManager import ModelManager
from src.AudioProcessor import AudioProcessor
from src.RecordingManager import RecordingManager

class MyWidget(QtWidgets.QWidget):
    
    model_name = None
    language = None
    model_list = None
    model_manager = None
    recording = False

    def __init__(self, config):
        super().__init__()

        self.config = config

        self.create_menu()
        self.create_horizontal_group_box()
        self.create_grid_group_box()
        self.textOutputs = QtWidgets.QPlainTextEdit("")
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

        self.setWindowTitle(self.config.get("window_title"))
        self.recording_manager = RecordingManager()

    def create_menu(self):
        self._menu_bar = QtWidgets.QMenuBar()

        self._file_menu = QtWidgets.QMenu("&File", self)
        self._exit_action = self._file_menu.addAction("E&xit")
        self._menu_bar.addMenu(self._file_menu)

    def create_horizontal_group_box(self):
        self._horizontal_group_box = QtWidgets.QGroupBox("Basic Components")
        layout = QtWidgets.QHBoxLayout()
        
        model_manager = ModelManager(self.config)
        self.model_list = model_manager.get_model_list(self)
        self.buttonModelOption = QtWidgets.QComboBox()
        self.buttonModelOption.addItems(self.model_list)
        layout.addWidget(self.buttonModelOption)

        self.buttonLanguageOption = QtWidgets.QComboBox()
        self.buttonLanguageOption.addItems(self.config.get("language_list"))
        layout.addWidget(self.buttonLanguageOption) 
        
        buttonSelectFile = QtWidgets.QPushButton("Select File")
        buttonSelectFile.clicked.connect(self.select_file)
        layout.addWidget(buttonSelectFile)
        
        
        buttonMicrophone = QtWidgets.QPushButton("Microphone On/Off")
        buttonMicrophone.clicked.connect(self.record_to_transcribe)
        layout.addWidget(buttonMicrophone)

        buttonClear = QtWidgets.QPushButton("Clear")
        buttonClear.clicked.connect(self.clear)
        layout.addWidget(buttonClear)

        self._horizontal_group_box.setLayout(layout)
    
    def create_grid_group_box(self):
        self._grid_group_box = QtWidgets.QGroupBox("Advanced Controls")
        layout = QtWidgets.QGridLayout()

        self.checkboxAuto = QtWidgets.QCheckBox("Auto Scroll")
        layout.addWidget(self.checkboxAuto, 1, 0)

        self.checkboxDetection = QtWidgets.QCheckBox("Detection")
        layout.addWidget(self.checkboxDetection, 2, 0)
        
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
    def clear(self):
        self.textOutputs.setPlainText("")
    
    @QtCore.Slot()
    def download_model(self):
        model_manager = ModelManager(self.config)
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
            audio_processor = AudioProcessor(self.model_name, self.language)
            audio_data = audio_processor.preprocess_audio(file_path)
            try:
                QtWidgets.QMessageBox.warning(None, "Warning", "Trascription is processing... Please wait...")
                start_time = time.time()
                trascription = audio_processor.transcribe_audio(audio_data)
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

        self.recording = not self.recording

        if self.recording:
            self.model_name = self.buttonModelOption.currentText()
            self.language = self.buttonLanguageOption.currentText()
            self.input_device_info = None
            
            from PySide6.QtWidgets import QInputDialog, QMessageBox
            from PySide6.QtMultimedia import QMediaDevices  
            devices = QMediaDevices.audioInputs()
            device_names = [device.description() for device in devices]
            if not device_names:
                QMessageBox.warning(self, "No Devices Detected")

            item, ok = QInputDialog.getItem(
                self, 
                "Selection", 
                "Please select an audio recording input: ", 
                device_names, 
                editable=False
            )

            if ok and item:
                device_info = self.recording_manager.get_pyaudio_device_info(item)
                if device_info:
                    QMessageBox.information(self, "Selected", f"Selected Input Device: \n{item}")
                    print(f"User selected input device:{item}")
                    self.input_device_info = device_info
                else:
                    QMessageBox.warning(self, "Failed", "No corresponding PyAudio device found")
            else:
                QMessageBox.information(self, "Canceled")

            input_device = self.input_device_info
            if self.checkboxDetection.isChecked():
                silence_timeout = self.config.get('silence_timeout')
            else:
                silence_timeout = 10000
            try:
                self.textStatus.setText("Recording...")
                self.recording_manager.start_recording(input_device, self.model_name, self.language, record_seconds=self.config.get('record_seconds'), silence_timeout=silence_timeout)
                self.recording_manager.transcription_updated.connect(self.append_transcription)
                self.recording_manager.recording_stopped.connect(self.on_recording_stopped)
            except Exception as e:
                QMessageBox.critical(self, "Recording Failed", str(e))
        else:
            self.recording_manager.stop_recording()
            self.recording_manager.recording_stopped.connect(self.on_recording_stopped)

    def append_transcription(self, text):
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.textOutputs.appendPlainText(f"[{timestamp}] {text}")

        if self.checkboxAuto.isChecked():
            self.textOutputs.moveCursor(QTextCursor.End)
            self.textOutputs.ensureCursorVisible()
    
    @QtCore.Slot()
    def on_recording_stopped(self):
        self.textStatus.setText("Recording stopped.")
