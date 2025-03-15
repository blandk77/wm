import os
import logging
from pyrogram import Client
from pyrogram.types import Message
import ffmpeg
import subprocess

logging.basicConfig(level=logging.INFO)

def add_overlay(client: Client, message: Message, overlay_image_id, user_id):
    # Download the overlay image
    logging.info("Downloading overlay image...")
    overlay_image = client.download_media(overlay_image_id)

    # Download the video
    logging.info("Downloading video...")
    video = client.download_media(message)

    # Overlay the image on the video using ffmpeg
    logging.info("Overlaying image on video...")
    output_video = os.path.join("/app", f"{user_id}.mp4")
    command = f"ffmpeg -i {video} -i {overlay_image} -filter_complex overlay -map_metadata 0 -c:v copy -c:a copy {output_video}"
    subprocess.run(command, shell=True)
    # Send the output video with the original caption
    logging.info("Sending output video...")
    caption = message.caption
    client.send_video(message.chat.id, video=output_video, caption=caption)
