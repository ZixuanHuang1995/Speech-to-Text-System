class AudioProcessor:
    filepath = None
        
    def __init__(self):
        pass

    def preprocess_audio(self, filepath):
        self.filepath = filepath
        import librosa
        raw_speech, samplerate = librosa.load(filepath, sr=16000)
        return raw_speech

    def transcribe_audio(self, audio_data, model_name, language):
        if model_name.startswith("OpenVINO/"):
            return self.__transcribe_audio_vino(audio_data, model_name, language)
        else:
            return self.__transcribe_audio_whisper(audio_data, model_name, language)
        
    def __transcribe_audio_vino(self, audio_data, model_name, language):
        model_path = "models/" + model_name
        language_key = "<|" + language + "|>"
        import openvino_genai as ov_genai
        pipe = ov_genai.WhisperPipeline(model_path, "CPU")
        result = pipe.generate(audio_data.tolist(), max_new_tokens=100, language = language_key) # max_new_tokens 決定文字生成的長度
        return result.texts[0]
    
    def __transcribe_audio_whisper(self, audio_data, model_name, language):
        import whisper
        import numpy as np
        model = whisper.load_model(model_name, "cpu").eval()
        if audio_data.dtype != np.float32:
            audio_data = audio_data.astype(np.float32)
        result= model.transcribe(audio=audio_data, fp16=False, language=language)["text"] 
        return result
