from whisper import _MODELS
import ipywidgets as widgets
import openvino as ov
import time

# Accelerate inference with OpenVINO
import huggingface_hub as hf_hub

model_id = "OpenVINO/whisper-medium-fp16-ov"
model_path = "whisper-medium-fp16-ov"

hf_hub.snapshot_download(model_id, local_dir=model_path)

import openvino_genai as ov_genai
import librosa

def read_wav(filepath):
  raw_speech, samplerate = librosa.load(filepath, sr=16000)
  return raw_speech.tolist()

def transcribe(raw_speech):
  pipe = ov_genai.WhisperPipeline(model_path, "CPU")
  result = pipe.generate(raw_speech, max_new_tokens=100)
  print(result)

raw_speech = read_wav("Winter.mp3")
start_time = time.time()
transcribe(raw_speech)
end_time = time.time()
print("large 加速執行時間（英文）：", end_time - start_time, "秒")

raw_speech = read_wav("train.mp3")
start_time = time.time()
transcribe(raw_speech)
end_time = time.time()
print("large 加速執行時間（中文）：", end_time - start_time, "秒")

model_id = widgets.Dropdown(
    options=list(_MODELS),
    value='medium', # ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large']
    description='Model:',
    disabled=False,
)

# No accelerate inference with OpenVINO
# Instantiate model
import whisper
model = whisper.load_model(model_id.value, "cpu")
model.eval()
pass

# task
task = widgets.Select(
    options=["transcribe", "translate"],
    value="transcribe",
    description="Select task:",
    disabled=False
)
task

start_time = time.time()
audio = "Winter.mp3"
transcription = model.transcribe(audio, task=task.value)
print(transcription["text"])
end_time = time.time()
print("large 正常執行時間（英文）：", end_time - start_time, "秒")

start_time = time.time()
audio = "train.mp3"
transcription = model.transcribe(audio, task=task.value)
print(transcription["text"])
end_time = time.time()
print("large 正常執行時間（中文）：", end_time - start_time, "秒")
