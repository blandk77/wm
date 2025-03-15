import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import MongoDB
from utils import add_overlay, remove_overlay

logging.basicConfig(level=logging.INFO)

app = Client("telegram_bot", api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)

mongo_db = MongoDB(config.MONGO_URI, config.MONGO_DB_NAME, config.MONGO_COLLECTION_NAME)

@app.on_message(filters.command("start"))
def start_cmd(client, message):
    message.reply("Hello! I'm a Telegram bot that adds image overlays to videos.")

@app.on_message(filters.command("add"))
def add_overlay_cmd(client, message):
    if message.reply_to_message and message.reply_to_message.media:
        overlay_image = message.reply_to_message.media
        mongo_db.add_overlay_image(overlay_image)
        message.reply("Overlay image added successfully!")
    else:
        message.reply("Please reply to a media message (image) to add it as an overlay.")

@app.on_message(filters.command("remove"))
def remove_overlay_cmd(client, message):
    if message.reply_to_message and message.reply_to_message.media:
        overlay_image = message.reply_to_message.media
        mongo_db.remove_overlay_image(overlay_image)
        message.reply("Overlay image removed successfully!")
    else:
        message.reply("Please reply to a media message (image) to remove it as an overlay.")

@app.on_message(filters.video | filters.document)
def process_video(client, message):
    message.reply("Please wait...")
    try:
        overlay_image = mongo_db.get_overlay_image()
        if overlay_image:
            output_video = add_overlay(message.media, overlay_image)
            client.send_video(message.chat.id, output_video)
        else:
            message.reply("No overlay image found.")
    except Exception as e:
        message.reply(f"Error: {str(e)}")

if __name__ == "__main__":
    app.run()
