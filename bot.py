import os
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, MAX_VIDEO_SIZE, TEMP_DIR
from utils import add_overlay, ensure_temp_dir_exists

# Ensure temporary directory exists
ensure_temp_dir_exists(TEMP_DIR)

# Initialize the bot
app = Client("video_overlay_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start") & filters.private)
async def start(client, message: Message):
    await message.reply(
        "👋 Hi! I’m a bot that can add a transparent image overlay (with text) to your videos.\n\n"
        "📥 Send me a video to get started!"
    )

@app.on_message(filters.video & filters.private)
async def process_video(client, message: Message):
    video = message.video

    # Check video size
    if video.file_size > MAX_VIDEO_SIZE:
        await message.reply("❌ The video is too large! Please send a video smaller than 50 MB.")
        return

    # Download the video
    video_path = await message.download(file_name=os.path.join(TEMP_DIR, "input_video.mp4"))
    await message.reply("✅ Video received! Now please send me the transparent image overlay (with text).")

    # Wait for overlay image from the user
    overlay_message = await client.listen(message.chat.id, filters.photo, timeout=300)
    if not overlay_message:
        await message.reply("❌ You didn’t send an overlay image. Please try again.")
        return

    overlay_image_path = await overlay_message.download(file_name=os.path.join(TEMP_DIR, "overlay.png"))

    # Process the video
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
