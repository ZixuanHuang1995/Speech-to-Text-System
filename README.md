# Whisper GUI

### Accelerated Real-Time Speech Recognition 
Stacks:
1. OpenAI’s Whisper model
2. Intel's OpenVINO toolkit
3. Qt for Python

This application supports both file-based transcription and real-time microphone recording with transcription capabilities. 

### Architecture Design 
The system is organized into four main components:
1. UI Layer (MyWidget): The graphical user interface implemented using PySide6 (Qt for Python). 
2. Recording Manager: Handles microphone recording with real-time processing. 
3. Model Manager: Manages model downloading, storage, and loading. 
4. Audio Processor: Processes audio data and performs transcription. 

### Use Cases 
1. File Transcription Workflow
<img width="1399" alt="File Transcription Workflow" src="https://github.com/user-attachments/assets/7017256b-1558-434b-a0c2-fb075ed85046" />

2. Real-time Recording and Transcription Workflow
<img width="1399" alt=" Real-time Recording and Transcription Workflow" src="https://github.com/user-attachments/assets/0518bca0-da84-46df-8d9e-bc6fcf7268ee" />


For detailed documentation, see https://deepwiki.com/ZixuanHuang1995/OpenVINO
