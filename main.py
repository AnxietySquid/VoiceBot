from typing import Final
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final = os.getenv("BOT_TOKEN")  
BOT_USERNAME: Final = '@auto_voice_bot'
VOICE_MESSAGES_PATH: Final = "./voices"
DEFAULT_USER_VOICE_DURATION: Final = 60

os.makedirs(VOICE_MESSAGES_PATH, exist_ok=True)

# Commands

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me a voice message and a text right after!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here are the instructions")


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Here is the custom command")

# Responses
# Process the text that the user sents

def handle_response(text: str) -> tuple[str, str]:

    processed: str = text.lower()

    if 'hello' in processed:
        return ('text', 'hello')

    if 'how are you' in processed:
        return ('text', 'fine')

    if 'music' in processed:
        return ('voice', 'example.mp3')

    return ('text', 'I do not understand you')



async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    # Debug
    print(f'User {update.message.chat.username} ({update.message.chat.id}) in {message_type} said: "{text}"')

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
            await update.message.reply_voice(voice=voice_file, caption="Here you go")

    print(f'Bot responded with {response_type}: {response_value}')

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file_id = voice.file_id
    duration = voice.duration

    # Get file
    file = await context.bot.get_file(file_id)
    if int(duration) <= DEFAULT_USER_VOICE_DURATION:
        # Save file
        file_path = f"voice_{update.message.chat.id}_{voice.file_unique_id}.ogg"
        await file.download_to_drive(VOICE_MESSAGES_PATH + "/" + file_path)
        # Debug
        print(f"Saved voice message from {update.message.chat.username} as {file_path}")
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
    app.add_handler(CommandHandler('custom', custom_command))


    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # Errors
    app.add_error_handler(error)

    # Checks messgaes every n seconds 
    # Debug
    print('Polling...')
    app.run_polling(poll_interval=3)












