# Voice cloning telegram bot
[Перевод на русский здесь](#русский)  
  
This repository is an implementation of https://github.com/CorentinJ/Real-Time-Voice-Cloning real time voice cloning in a telegram bot format.  
Features:  

 - Basic TTS without the use of the model — voices your text over with gTTS
 - Voice cloning (voices over the text you send trying to mimic your voice)
 
 ---
## Usage
1. Create a bot using BotFather
2. Add commands `/start`, `/help`, `/tts` and `/clone`
3. Install **uv**
4. Clone the repository
5. Change directory to the cloned repository
6. Create a file named **.env** without quotes and insert your bot token: BOT_TOKEN="your bot token here" 
7. In the directory with the project run `uv run bot.py`  

If everything done correctly, your bot should be ready to take the messages  
>Note!
>First time launch requires downloading the models, it may take some time depending on your internet connection speed


Props to **https://github.com/CorentinJ/Real-Time-Voice-Cloning**; the voice cloning part was taken from this repo, modified and integrated.

---

## Русский

# Телеграм-бот для клонирования голоса  
  
Этот репозиторий представляет собой реализацию проекта [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning) в формате телеграм-бота.  
Возможности:  

 - Базовый TTS без использования модели — озвучивает ваш текст с помощью gTTS  
 - Клонирование голоса (озвучивает отправленный вами текст, стараясь имитировать ваш голос)
 
 ---
## Использование
1. Создайте бота с помощью **BotFather**  
2. Добавьте команды: `/start`, `/help`, `/tts` и `/clone`  
3. Установите **uv**  
4. Клонируйте репозиторий  
5. Перейдите в каталог с клонированным репозиторием  
6. Создайте файл с именем **.env** и вставьте туда ваш токен:  BOT_TOKEN="ваш токен сюда"
7. В каталоге с проектом выполните команду: `uv run bot.py`  
  
Если всё сделано правильно, ваш бот будет готов принимать сообщения.  

> **Примечание:**  
> При первом запуске потребуется загрузить модели, что может занять некоторое время в зависимости от скорости вашего интернет-соединения.

Спасибо **[https://github.com/CorentinJ/Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)** — часть, отвечающая за клонирование голоса, была взята из этого репозитория, изменена и интегрирована.
