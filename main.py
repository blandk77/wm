from pyrogram import Client, filters
from pyrogram.errors import UserDeactivatedBan, UserDeactivatedRestrict, UserDeactivatedScam
from database import MongoDB
from watermark import add_watermark
from config import API_ID, API_HASH, BOT_TOKEN

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message):
    try:
        message.reply("Welcome to the Watermark Bot! by @itsme123i")
    except (UserDeactivated, UserDeactivatedBan, UserDeactivatedRestrict, UserDeactivatedScam):
        pass

@app.on_message(filters.command("add"))
def add_command(client, message):
    try:
        message.reply("Please send me the watermark URL.")
    except (UserDeactivated, UserDeactivatedBan, UserDeactivatedRestrict, UserDeactivatedScam):
        pass

@app.on_message(filters.regex(r"^https?://"))
def handle_watermark_url(client, message):
    try:
        url = message.text
        mongo_db = MongoDB()
        mongo_db.save_watermark_url(url, message.from_user.id)
        message.reply("Watermark URL saved!")
    except (UserDeactivated, UserDeactivatedBan, UserDeactivatedRestrict, UserDeactivatedScam):
        pass

@app.on_message(filters.video)
def handle_file(client, message):
    try:
        file_id = message.video.file_id
        file = client.download_media(file_id)
        mongo_db = MongoDB()
        watermark_url = mongo_db.get_watermark_url(message.from_user.id)
        add_watermark(file, watermark_url)
        client.send_video(message.from_user.id, "output.mp4")
    except (UserDeactivated, UserDeactivatedBan, UserDeactivatedRestrict, UserDeactivatedScam):
        pass

if __name__ == "__main__":
    app.run()
