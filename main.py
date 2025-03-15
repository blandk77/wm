import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
from utils import add_overlay
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

logging.basicConfig(level=logging.INFO)

app = Client("telegram_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

@app.on_message(filters.command("start"))
def start_cmd(client, message):
    message.reply("Hello! I'm a Telegram bot that adds image overlays to videos.")

@app.on_message(filters.command("add"))
def add_overlay_cmd(client, message):
    if message.reply_to_message and message.reply_to_message.photo:
        overlay_image = message.reply_to_message.photo.file_id
        user_id = message.from_user.id
        collection.update_one({"user_id": user_id}, {"$set": {"overlay_image": overlay_image}}, upsert=True)
        message.reply("Overlay image added successfully!")
    else:
        message.reply("Please reply to a photo message to add it as an overlay.")

@app.on_message(filters.command("remove"))
def remove_overlay_cmd(client, message):
    user_id = message.from_user.id
    collection.delete_one({"user_id": user_id})
    message.reply("Overlay image removed successfully!")

@app.on_message(filters.video | filters.document)
def process_video(client, message):
    user_id = message.from_user.id
    user_data = collection.find_one({"user_id": user_id})
    if user_data and "overlay_image" in user_data:
        overlay_image_id = user_data["overlay_image"]
        message.reply("Please wait...")
        try:
            output_video = add_overlay(client, message, overlay_image_id, user_id)
            client.send_video(message.chat.id, output_video)
        except Exception as e:
            message.reply(f"Error: {str(e)}")
    else:
        message.reply("No overlay image found.")

if __name__ == "__main__":
    app.run()
