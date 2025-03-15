import os
from pyrogram import Client

def add_overlay(client: Client, message: Message, overlay_image_id, user_id):
    # Download the overlay image
    overlay_image = client.download_media(overlay_image_id)

    # Download the video
    video = client.download_media(message)

    # Save the overlay image to the server
    output_image = os.path.join("/app", f"{user_id}.jpg")
    os.rename(overlay_image, output_image)

    # Add the overlay to the video
    output_video = os.path.join("/app", f"{user_id}.mp4")
    # Use your preferred method to add the overlay to the video
    # For example, using ffmpeg:
    os.system(f"ffmpeg -i {video} -i {output_image} -c:v libx264 -crf 18 {output_video}")

    # Clean up
    os.remove(video)

    return output_video
