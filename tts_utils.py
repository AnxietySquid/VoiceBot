import os
from pathlib import Path
from gtts import gTTS

PROJECT_ROOT = Path(__file__).resolve().parent
os.makedirs(PROJECT_ROOT / "voiced_messages", exist_ok=True)
print(f'PROJECT ROOT!!!!!!! {PROJECT_ROOT}')
lowercase_alphabet_ru = [chr(i) for i in range(ord('а'), ord('я') + 1)]
uppercase_alphabet_ru = [chr(i) for i in range(ord('А'), ord('Я') + 1)]    

def text_to_speech(text: str, filename: str = "output.mp3") -> str:
    file_path = PROJECT_ROOT / "voiced_messages" / filename

    # Language check
    if any(letter in text for letter in lowercase_alphabet_ru) or any(letter in text for letter in uppercase_alphabet_ru):
        lang = "ru"
    else:
        lang = "en"

    # Debug
    print(f"Detected language: {lang}")

    tts = gTTS(text, lang=lang)
    tts.save(file_path)
    return file_path