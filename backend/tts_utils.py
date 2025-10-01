import os
from pathlib import Path
from gtts import gTTS

PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
os.makedirs(PROJECT_ROOT + "/backend/voiced_messages", exist_ok=True)

def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    file_path = PROJECT_ROOT + "/backend/voiced_messages/" + filename
    tts = gTTS(text, lang="en")
    tts.save(file_path)
    return file_path
