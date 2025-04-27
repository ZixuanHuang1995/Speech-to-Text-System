from src.AudioProcessor import AudioProcessor
from PySide6.QtCore import QObject, Signal
import threading
import numpy as np

class RecordingManager(QObject):
    transcription_updated = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.trascription = ''
        self.record_thread = None
        self.frames = []

    def start_recording(self, input_device, model_name):
        import pyaudio
        audio_processor = AudioProcessor()

        self.input_device = input_device
        self.recording = True

        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      input_device_index = 1,
                                      frames_per_buffer=1024)

        def record():
            while self.recording:
                data = self.stream.read(1024)
                self.frames.append(data)
                if len(self.frames) > 0:
                    audio_bytes = b''.join(self.frames)
                    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)
                    audio_data = audio_processor.preprocess_audio(audio_np)
                    self.trascription = audio_processor.transcribe_audio(audio_data, model_name)
                    self.frames = []
                self.transcription_updated.emit(self.trascription)

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()
        
    def stop_recording(self):
        self.recording = False
        self.record_thread.join()
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()
    
    @staticmethod
    def get_input_devices():
        import pyaudio
        p = pyaudio.PyAudio()
        devices = []
        for i in range(p.get_device_count()):
            device_info = p.get_device_info_by_index(i)
            if device_info['maxInputChannels'] > 0:
                devices.append(device_info)
        return devices
