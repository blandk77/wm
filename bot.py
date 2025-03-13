import os
import logging
from telegram import Update, Filters
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

logging.basicConfig(level=logging.INFO)

from config import TOKEN, MONGO_URI
from database import MongoDB
from watermark import add_watermark

def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the Watermark Bot!')

def ask_watermark_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please send me the watermark URL.')

def handle_watermark_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = update.message.text
    mongo_db = MongoDB(MONGO_URI)
    mongo_db.save_watermark_url(url, update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Watermark URL saved!')

def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    file_id = update.message.video.file_id
    file = context.bot.get_file(file_id)
    file.download('input.mp4')
    mongo_db = MongoDB(MONGO_URI)
    watermark_url = mongo_db.get_watermark_url(update.effective_chat.id)
    add_watermark('input.mp4', watermark_url)
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    add_handler = CommandHandler('add', ask_watermark_url)
    message_handler = MessageHandler(Filters.TEXT & ~Filters.COMMAND, handle_watermark_url)
    video_handler = MessageHandler(Filters.VIDEO, handle_file)

    application.add_handler(start_handler)
    application.add_handler(add_handler)
    application.add_handler(message_handler)
    application.add_handler(video_handler)

    application.run_polling()

if __name__ == '__main__':
    main()
