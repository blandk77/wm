import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import MongoDB
from utils import add_overlay
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

logging.basicConfig(level=logging.INFO)

class Bot:
    def __init__(self):
        self.app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
        self.mongo_db = MongoDB(MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME)

        self.app.add_handler(filters.command("start"), self.start_cmd)
        self.app.add_handler(filters.command("add"), self.add_overlay_cmd)
        self.app.add_handler(filters.command("remove"), self.remove_overlay_cmd)
        self.app.add_handler(filters.video | filters.document, self.process_video)

    def start_cmd(self, client, message):
        message.reply("Hello! I'm a Telegram bot that adds image overlays to videos.")

    def add_overlay_cmd(self, client, message):
        if message.reply_to_message and message.reply_to_message.photo:
            overlay_image = message.reply_to_message.photo.file_id
            user_id = message.from_user.id
            self.mongo_db.add_overlay_image(user_id, overlay_image)
            message.reply("Overlay image added successfully!")
        else:
            message.reply("Please reply to a photo message to add it as an overlay.")

    def remove_overlay_cmd(self, client, message):
        user_id = message.from_user.id
        self.mongo_db.collection.delete_one({"user_id": user_id})
        message.reply("Overlay image removed successfully!")

    def process_video(self, client, message):
        user_id = message.from_user.id
        overlay_image_id = self.mongo_db.get_overlay_image(user_id)
        if overlay_image_id:
            message.reply("Please wait...")
            try:
                output_video = add_overlay(client, message, overlay_image_id, user_id)
                client.send_video(message.chat.id, output_video)
            except Exception as e:
                message.reply(f"Error: {str(e)}")
        else:
            message.reply("No overlay image found.")

    def run(self):
        self.app.run()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
