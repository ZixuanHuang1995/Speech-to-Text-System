class AudioProcessor:
    filepath = None
        
    def __init__(self):
        pass

    def preprocess_audio(self, filepath):
        self.filepath = filepath
        import librosa
        raw_speech, samplerate = librosa.load(filepath, sr=16000)
        return raw_speech

    def transcribe_audio(self, audio_data, model_name):
        if model_name.startswith("OpenVINO/"):
            return self.__transcribe_audio_vino(audio_data, model_name)
        else:
            return self.__transcribe_audio_whisper(audio_data, model_name)
        
    def __transcribe_audio_vino(self, audio_data, model_name):
        model_path = "models/" + model_name
        import openvino_genai as ov_genai
        pipe = ov_genai.WhisperPipeline(model_path, "CPU")
        result = pipe.generate(audio_data.tolist(), max_new_tokens=100)
        return result.texts[0]
    
    def __transcribe_audio_whisper(self, audio_data, model_name):
        import whisper
        model = whisper.load_model(model_name, "cpu").eval()
        result= model.transcribe(self.filepath)["text"] 
        return result
