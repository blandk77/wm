from pyrogram import Client, filters
import logging
from database import MongoDB
from watermark import add_watermark
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URL

logging.basicConfig(level=logging.INFO)

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message):
    try:
        message.reply("Welcome to the Watermark Bot! \nUnder development\n@Itsme123i")
    except Exception as e:
        logging.error(e)

@app.on_message(filters.command("add"))
def add_command(client, message):
    try:
        message.reply("Please send me the watermark URL.")
    except Exception as e:
        logging.error(e)

@app.on_message(filters.regex(r"^https?://"))
def handle_watermark_url(client, message):
    try:
        url = message.text
        mongo_db = MongoDB(MONGO_URL)
        mongo_db.save_watermark_url(url, message.from_user.id)
        message.reply("Watermark URL saved!")
    except Exception as e:
        logging.error(e)

@app.on_message(filters.video | filters.document)
def handle_file(client, message):
    try:
        file_id = message.video.file_id if message.video else message.document.file_id
        file = client.download_media(file_id)
        mongo_db = MongoDB(MONGO_URL)
        watermark_url = mongo_db.get_watermark_url(message.from_user.id)
        add_watermark(file, watermark_url)
        client.send_video(message.from_user.id, "output.mp4")
    except Exception as e:
        logging.error(e)

@app.on_message(filters.command("remove"))
def remove_command(client, message):
    try:
        mongo_db = MongoDB(MONGO_URL)
        mongo_db.remove_watermark_url(message.from_user.id)
        message.reply("Watermark URL removed!")
    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    app.run()
