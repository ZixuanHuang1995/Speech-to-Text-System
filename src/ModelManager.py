import os
import whisper
import huggingface_hub as hf_hub
import openvino_genai as ov_genai

class ModelManager:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_model_list() -> list:
        whisper_models = ['tiny.en', 'tiny', 'base']
        openvino_whisper_models = [
            "OpenVINO/whisper-tiny-fp16-ov",
            "OpenVINO/whisper-base-fp16-ov",
            "OpenVINO/whisper-large-v3-int4-ov",
            "OpenVINO/whisper-large-v3-fp16-ov"
        ]
        return whisper_models + openvino_whisper_models
    
    def is_model_available(self, model_name) -> bool:
        # Check if the model is available in the local directory
        return os.path.exists(f"models/{model_name}")
    
    def download_model(self, model_list): 
        for model_name in model_list:
            print("=====" + model_name + "=====")
            if not self.is_model_available(str(model_name)):
                model_path = "models/" + model_name
                if model_name.startswith("OpenVINO/"):
                    print(f"Download OpenVINO Whisper Model：{model_name} ...")
                    model_id = model_name
                    hf_hub.snapshot_download(model_id, local_dir=model_path)
                else:
                    print(f"Download Whisper Model：{model_name} ...")
                    from whisper import _download, _MODELS
                    _download(_MODELS[model_name], "models/", False)
                print(f"Model {model_name} downloaded and saved to {model_path}")
            else:
                print(f"{model_name} already exists in the local directory.")
        

    def load_model(self, model_name):
        model_path = "models/" + model_name
        if model_name.startswith("OpenVINO/"):
            pipe = ov_genai.WhisperPipeline(model_path, "CPU")
            return pipe
        else:
            model = whisper.load_model(model_path, "cpu")
            model.eval()
            return model



