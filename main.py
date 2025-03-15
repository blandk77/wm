import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import MongoDB
from utils import add_overlay
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

logging.basicConfig(level=logging.INFO)

app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

mongo_db_instance = MongoDB(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME)

@app.on_message(filters.command("start"))
def start_cmd(client, message):
    message.reply("Hello! I'm a Telegram bot that adds image overlays to videos.")

@app.on_message(filters.command("add"))
def add_overlay_cmd(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        overlay_image = message.reply_to_message.photo.file_id
        mongo_db_instance.add_overlay_image(overlay_image)
        message.reply("Overlay image added successfully!")
    else:
        message.reply("Please reply to a photo message to add it as an overlay.")

@app.on_message(filters.command("remove"))
def remove_overlay_cmd(client, message):
    mongo_db_instance.remove_overlay_image()
    message.reply("Overlay image removed successfully!")

@app.on_message(filters.video | filters.document)
def process_video(client, message):
    overlay_image = mongo_db_instance.get_overlay_image()
    if overlay_image:
        message.reply("Please wait...")
        try:
            output_video = add_overlay(client, message, overlay_image)
            client.send_video(message.chat.id, output_video)
        except Exception as e:
            message.reply(f"Error: {str(e)}")
    else:
        message.reply("No overlay image found.")

if __name__ == "__main__":
    app.run()
