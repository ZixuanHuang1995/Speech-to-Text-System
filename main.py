import sys
from PySide6 import QtWidgets
from src.ui.QtMain import MyWidget

import json
import os
import sys

def load_config():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    config_path = os.path.join(base_path, 'config.json')

    default_config = {
        "whisper_models": ['base'],
        "openvino_whisper_models": [
            "OpenVINO/whisper-tiny-fp16-ov",
            "OpenVINO/whisper-base-fp16-ov",
            "OpenVINO/whisper-medium-fp16-ov", 
            "OpenVINO/whisper-large-v3-int4-ov",
            "OpenVINO/whisper-large-v3-fp16-ov"
        ],
        "language_list": ['zh', 'en', 'ja', 'ko'],
        "record_seconds": 3,
        "silence_timeout": 10,
        "window_title": "OpenVINO Whisper GUI",
        "window_size_width": 800,
        "window_size_high": 600,
    }

    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2)

    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    config=load_config()
    widget = MyWidget(config)
    widget.resize(config.get('window_size_width'), config.get('window_size_high'))
    widget.show()
    
    sys.exit(app.exec())