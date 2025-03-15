import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, TEMP_DIR
from utils import add_overlay, ensure_temp_dir_exists
from database import save_overlay, get_overlay, remove_overlay
import time
import requests

# Synchronize time with an NTP server
def synchronize_time():
    try:
        # Fetch time from a public NTP server or API
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
        response.raise_for_status()
        utc_time = response.json()["unixtime"]

        # Set the system time (only works in Python runtime)
        time_offset = utc_time - int(time.time())
        print(f"Synchronized time with UTC. Time offset: {time_offset} seconds.")
    except Exception as e:
        print(f"Failed to synchronize time: {e}")

synchronize_time()

# Ensure temporary directory exists
ensure_temp_dir_exists(TEMP_DIR)

# Initialize the bot
app = Client("video_overlay_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply(
        "👋 Hi! I’m a bot that can add a transparent image overlay (with text) to your videos.\n\n"
        "📥 Use /add to upload your overlay image.\n"
        "❌ Use /remove to delete your overlay image.\n"
        "📥 Send me a video or document file, and I’ll apply your overlay!"
    )

@app.on_message(filters.command("add") & filters.private)
async def add_overlay_command(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply("❌ Please reply to a transparent image (.jpg) to add it as your overlay.")
        return

    # Save the overlay image to the database
    file_id = message.reply_to_message.photo.file_id
    save_overlay(message.from_user.id, file_id)
    await message.reply("✅ Overlay image added successfully!")

@app.on_message(filters.command("remove") & filters.private)
async def remove_overlay_command(client, message: Message):
    remove_overlay(message.from_user.id)
    await message.reply("✅ Overlay image removed successfully!")

@app.on_message(filters.video | filters.document & filters.private)
async def process_video(client, message: Message):
    # Retrieve overlay image from the database
    file_id = get_overlay(message.from_user.id)
    if not file_id:
        await message.reply("❌ You don’t have an overlay image. Use /add to upload one.")
        return

    # Download the overlay image
    overlay_image_path = os.path.join(TEMP_DIR, "overlay.jpg")
    await client.download_media(file_id, file_name=overlay_image_path)

    # Download the video
    video_path = await message.download(file_name=os.path.join(TEMP_DIR, "input_video.mp4"))
    output_path = os.path.join(TEMP_DIR, "output_video.mp4")

    try:
        await message.reply("⏳ Processing your video. Please wait...")
        processed_video_path = add_overlay(video_path, overlay_image_path, output_path)
        await message.reply_video(processed_video_path)
    except Exception as e:
        await message.reply(f"❌ Failed to process the video: {e}")
    finally:
        # Clean up temporary files
        os.remove(video_path)
        os.remove(overlay_image_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# Run the bot
app.run()
