# make it work for universal paths and OSes
# make README
# make clearer instructions to use the bot
# double the instructions in Russian?
# write logs
# save voice messages for future use
# make instruction to generate multiple voices over one voice message
# edge cases / error handling with user

from typing import Final
import os
import shutil
from pathlib import Path
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    ConversationHandler,
    filters, 
    ContextTypes
)
from voice_clone import init_models
from voice_clone import synthesize_to_file

from dotenv import load_dotenv

from tts_utils import text_to_speech

load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")  
BOT_USERNAME: Final = '@auto_voice_bot'
PROJECT_ROOT = Path(__file__).resolve().parent
VOICE_MESSAGES_PATH: Final = PROJECT_ROOT / "voices"
VOICE_MESSAGES_HISTORY_PATH = PROJECT_ROOT / "voices_history"

DEFAULT_USER_VOICE_DURATION: Final = 600

os.makedirs(VOICE_MESSAGES_PATH, exist_ok=True)

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug
    print(f'Command "start" has been invoked by user "{update.message.chat.username}"' )
    await update.message.reply_text("Hello! Send me a voice message and a text right after!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug
    print(f'Command "help" has been invoked by user "{update.message.chat.username}"' )
    await update.message.reply_text("Here are the instructions")


async def tts_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug
    print(f'Command "tts" has been invoked by user "{update.message.chat.username}"' )
    await update.message.reply_text("Send me the text and I will voice it over!")
    context.user_data["awaiting_tts"] = True

async def clone_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Debug
    print(f'Command "clone" has been invoked by user "{update.message.chat.username}"' )
    await update.message.reply_text(f"First I need a voice message (if you haven't send it before). The longer the voice message the better (not longer than {DEFAULT_USER_VOICE_DURATION/60} minutes.)")
    context.user_data["awaiting_clone"] = True

# Responses
# Process the text that the user sents

def handle_response(text: str) -> tuple[str, str]:

    processed: str = text.lower()

    if 'hello' in processed:
        return ('text', 'Hello! Want me to read your text outloud? Use the command /tts or /clone')

    if 'how are you' in processed:
        return ('text', "I'm fine")

    if 'music' in processed:
        return ('voice', 'example.mp3')

    return ('text', 'Use a command and choose what you wanna do!')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Handles user messages 
    '''
    message_type: str = update.message.chat.type
    text: str = update.message.text
    # Debug
    print(f'User {update.message.chat.username} ({update.message.chat.id}) in {message_type} said: "{text}"')

    if context.user_data.get("awaiting_tts"):
        context.user_data["awaiting_tts"] = False  # reset flag

        file_path = text_to_speech(text, f"{update.message.chat.id}_tts.mp3")
        with open(file_path, "rb") as voice_file:
            await update.message.reply_voice(voice=voice_file, caption="Here is the result")
            #Debug
            print(f'The voice message {update.message.chat.id}_tts.mp3 was sent to {update.message.chat.username}')
        return
    
    if context.user_data.get("awaiting_clone"):
        context.user_data["awaiting_clone"] = False  # reset flag

        await update.message.reply_text("Thanks, please wait a little, clearing my throat...")

        # Grab the voice msg and synthesize
        ref_audio = VOICE_MESSAGES_PATH / f"voice_{update.message.chat.id}.ogg"
        file_path = synthesize_to_file(ref_audio, text, output_path=VOICE_MESSAGES_PATH / f"voice_{update.message.chat.id}.wav")


        with open(file_path, "rb") as voice_file:
            await update.message.reply_voice(voice=voice_file, caption="Here is your cloned voice...\nYou can type /clone and send the text to use the same voice message")
            #Debug
            print(f'\nThe voice message {update.message.chat.id}_tts.wav was sent to {update.message.chat.username}')
        return

    # Will respond in group only if its name is in the message
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '').strip()
            response_type, response_value = handle_response(new_text)
        else:
            return
    else:
        response_type, response_value = handle_response(text)

    # Respond
    if response_type == 'text':
        await update.message.reply_text(response_value)
    elif response_type == 'voice':
        with open(response_value, "rb") as voice_file:
            await update.message.reply_voice(voice=voice_file, caption="Here is the result")
    # Debug
    print(f'Bot responded with {response_type}: {response_value}')

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    '''
    Handles user voice messages
    '''
    voice = update.message.voice
    file_id = voice.file_id
    duration = voice.duration

    # Get file
    file = await context.bot.get_file(file_id)
    if int(duration) <= DEFAULT_USER_VOICE_DURATION:
        # Save file
        file_path = f"voice_{update.message.chat.id}.ogg"
        await file.download_to_drive(VOICE_MESSAGES_PATH / file_path)
        # Save a copy with a more descriptive name
        file_path_history = f"voice_{update.message.chat.id}_{update.message.id}.ogg"
        os.makedirs(VOICE_MESSAGES_HISTORY_PATH, exist_ok=True)
        shutil.copy(VOICE_MESSAGES_PATH / file_path, VOICE_MESSAGES_HISTORY_PATH / file_path_history)

        # Debug
        print(f"Saved voice message from {update.message.chat.username} as {file_path_history}")
        if context.user_data.get("awaiting_clone"):
            await update.message.reply_text("Now send me the text you want me to read")

    else:
        # Debug
        print(f"Voice message from {update.message.chat.username} will not be saved (id = {voice.file_unique_id}), too long: {duration}s > {DEFAULT_USER_VOICE_DURATION}s") 
        await update.message.reply_text(f"Voice message is too long, make it {DEFAULT_USER_VOICE_DURATION}s or less")


# Debug
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    
    # Debug
    print('Starting bot')
    
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('tts', tts_command))
    app.add_handler(CommandHandler('clone', clone_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Errors
    app.add_error_handler(error)

    # Checks messgaes every n seconds 
    # Debug
    print('Polling...')
    app.run_polling(poll_interval=3)


