import whisper

model = whisper.load_model("turbo")

result = model.transcribe("train.mp3")
print(result["text"])

result2 = model.transcribe("Winter.mp3")
print(result2["text"])