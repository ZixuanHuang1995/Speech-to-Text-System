class AudioProcessor:
    filepath = None
    model_path = None
    model_name = None
    language_key = None
        
    def __init__(self, model_name, language):
        self.model_path = "models/" + model_name
        self.model_name = model_name
        self.language = language

        if self.model_name.startswith("OpenVINO/"):
            self.language_key = "<|" + language + "|>"
            import openvino_genai as ov_genai
            self.pipe = ov_genai.WhisperPipeline(self.model_path, "CPU")
        else:
            import whisper
            self.model = whisper.load_model(model_name, "cpu").eval()

    def preprocess_audio(self, filepath):
        self.filepath = filepath
        import librosa
        raw_speech, samplerate = librosa.load(filepath, sr=16000)
        return raw_speech

    def transcribe_audio(self, audio_data):
        if self.model_name.startswith("OpenVINO/"):
            return self.__transcribe_audio_vino(audio_data)
        else:
            return self.__transcribe_audio_whisper(audio_data)
        
    def __transcribe_audio_vino(self, audio_data):
        result = self.pipe.generate(audio_data, max_new_tokens=100, language = self.language_key) # max_new_tokens 決定文字生成的長度
        return result.texts[0]
    
    def __transcribe_audio_whisper(self, audio_data):
        import numpy as np
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        result= self.model.transcribe(audio=audio_data, fp16=False, language=self.language)["text"] 
        return result
