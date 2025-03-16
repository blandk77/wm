import os
import subprocess
from pyrogram import Client
from pyrogram.types import Message

def add_overlay(client: Client, message: Message, overlay_image_id, user_id):
    # Download the overlay image
    overlay_image = client.download_media(overlay_image_id)
    overlay_image = os.path.abspath(overlay_image)

    # Download the video
    video = client.download_media(message)
    video = os.path.abspath(video)

    # Define output file paths
    temp_output_path = os.path.abspath(os.path.join("/app", f"{user_id}_temp.mp4"))
    final_output_path = os.path.abspath(os.path.join("/app", f"{user_id}_final.mp4"))

    # Ensure the /app directory exists
    if not os.path.exists("/app"):
        os.makedirs("/app")

    # Use FFmpeg to overlay the image on the video
    ffmpeg_command = [
        "ffmpeg",
        "-i", video,            # Input video
        "-i", overlay_image,    # Input overlay image
        "-filter_complex", "overlay=W:H",  # Overlay the image (adjust position with W:H if needed)
        "-c:v", "copy",         # Copy the original video codec
        "-c:a", "copy",         # Copy the original audio codec
        "-map", "0",            # Map all streams (video, audio, subtitles)
        "-map", "1",            # Map the overlay image
        temp_output_path
    ]
    result = subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("FFmpeg Output:", result.stdout.decode())
    print("FFmpeg Errors:", result.stderr.decode())

    # Check if the temporary file was created
    if not os.path.exists(temp_output_path):
        raise FileNotFoundError(f"Temporary output file not found: {temp_output_path}")

    # Fix metadata using ffmpeg (final output)
    ffmpeg_metadata_command = [
        "ffmpeg",
        "-i", temp_output_path,
        "-c", "copy",           # Copy all streams without re-encoding
        "-movflags", "+faststart",
        final_output_path
    ]
    result = subprocess.run(ffmpeg_metadata_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("FFmpeg Metadata Output:", result.stdout.decode())
    print("FFmpeg Metadata Errors:", result.stderr.decode())

    # Check if the final file was created
    if not os.path.exists(final_output_path):
        raise FileNotFoundError(f"Final output file not found: {final_output_path}")

    # Send the output video
    client.send_video(message.chat.id, video=final_output_path)
