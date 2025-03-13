import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler
from pyrogram import filters 
from database import MongoDB
from watermark import add_watermark
from config import TOKEN, MONGO_URI

logging.basicConfig(level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Welcome to the Watermark Bot!')

def ask_watermark_url(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Please send me the watermark URL.')

def handle_watermark_url(update, context):
    url = update.message.text
    mongo_db = MongoDB(MONGO_URI)
    mongo_db.save_watermark_url(url, update.effective_chat.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Watermark URL saved!')

def handle_file(update, context):
    file_id = update.message.video.file_id
    file = context.bot.get_file(file_id)
    file.download('input.mp4')
    mongo_db = MongoDB(MONGO_URI)
    watermark_url = mongo_db.get_watermark_url(update.effective_chat.id)
    add_watermark('input.mp4', watermark_url)
    context.bot.send_video(chat_id=update.effective_chat.id, video=open('output.mp4', 'rb'))

def main():
    updater = Updater(TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('ask_watermark_url', ask_watermark_url))
    dp.add_handler(MessageHandler(Filters.text, handle_watermark_url))
    dp.add_handler(MessageHandler(Filters.video, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
