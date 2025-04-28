from src.AudioProcessor import AudioProcessor
from PySide6.QtCore import QObject, Signal
import threading
import numpy as np
import time

class RecordingManager(QObject):
    transcription_updated = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.trascription = ''
        self.is_recording = False
        self.record_thread = None
    
    def __is_silence(self, data, threshold=0.01):
        audio_chunk = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0  # normalization [-1.0, +1.0]
        rms = np.sqrt(np.mean(np.square(audio_chunk))) # calculate the RMS value of the volume
        return rms < threshold

    def start_recording(self, input_device, model_name, language, record_seconds=3, silence_timeout=10000):
        import pyaudio
        audio_processor = AudioProcessor(model_name, language)
        self.last_spoke_time = time.time()
        silence_timeout = silence_timeout

        self.input_device = input_device
        self.is_recording = True

        self.audio = pyaudio.PyAudio()
        channels = int(input_device['maxInputChannels'])
        self.rate = int(input_device['defaultSampleRate'])
        index = int(input_device['index'])
        self.frames_per_buffer = 1024
        self.record_seconds = record_seconds
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=channels,
                                      rate=self.rate,
                                      input=True,
                                      input_device_index = index,
                                      frames_per_buffer=self.frames_per_buffer)
        

        def record():
            while self.is_recording:
                frames = []
                num_frames = int(self.rate / self.frames_per_buffer * self.record_seconds)

                for _ in range(num_frames):
                    data = self.stream.read(self.frames_per_buffer, exception_on_overflow=False)

                    if not self.__is_silence(data):
                        self.last_spoke_time = time.time()

                    frames.append(np.frombuffer(data, dtype=np.int16))

                audio_np = np.concatenate(frames).astype(np.float32) / 32768.0  # normalization [-1.0, +1.0] 
                self.trascription = audio_processor.transcribe_audio(audio_np) 
                self.transcription_updated.emit(self.trascription) 

                # if silence_timeout
                if time.time() - self.last_spoke_time > silence_timeout:
                    print("Detected silence > 10s, stopping recording...")
                    self.transcription_updated.emit("Detected silence > 10s, stopping recording...") 
                    self.stop_recording()

        self.record_thread = threading.Thread(target=record)
        self.record_thread.start()

        
    def stop_recording(self):
        self.is_recording = False
        if self.record_thread is not None:
            self.record_thread.join()
    
    @staticmethod
    def get_pyaudio_device_info(target_name):
        import pyaudio
        p = pyaudio.PyAudio()
        target_name = target_name.lower().strip()

        for i in range(p.get_device_count()):
            info = p.get_device_info_by_index(i)
            name = info['name'].lower().strip()
            if target_name in name or name in target_name:
                info['index'] = i 
                p.terminate()
                return info
        
        p.terminate()
        return None
