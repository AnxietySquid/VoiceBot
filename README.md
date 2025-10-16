# Voice cloning telegram bot
[Перевод на русский здесь](#русский)  
This repository is an implementation of https://github.com/CorentinJ/Real-Time-Voice-Cloning real time voice cloning in a telegram bot format.  
Features:  

 - Basic TTS without the use of the model — voices your text over with gTTS
 - Voice cloning (voices over the text you send trying to mimic your voice)
 
 ---
## Usage
1. Create a bot using BotFather
2. Add commands /start, /help, /tts and /clone
3. Install uv
4. Clone the repository
5. Change directory to the cloned repository
6. Create a file named ".env" without quotes and insert your bot token: BOT_TOKEN="your bot token here" 
7. In the directory with the project run 
```
uv run bot.py
```
If everything done correctly, your bot should be ready to take the messages  
>Note!
>First time launch requires downloading the models, it may take some time depending on your internet connection speed


Props to **https://github.com/CorentinJ/Real-Time-Voice-Cloning**; the voice cloning part was taken from this repo, modified and integrated.

---

## Русский