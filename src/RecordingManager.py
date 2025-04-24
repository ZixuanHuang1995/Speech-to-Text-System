from src.AudioProcessor import AudioProcessor
from PySide6.QtCore import Signal

class RecordingManager:
    transcription_updated = Signal(str)
    
    def __init__(self):
        self.trascription = ''

    def start_recording(self, input_device, model_name):
        import pyaudio
        import threading

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
                self.trascription = audio_processor.transcribe_audio(data, model_name)
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
