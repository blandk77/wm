import os
import cv2
import numpy as np
import subprocess
from pyrogram import Client
from pyrogram.types import Message

def fix_video_metadata(input_path, output_path):
    subprocess.run([
        "ffmpeg", "-i", input_path, "-vcodec", "copy", "-acodec", "copy", "-crf", "0", output_path
    ])

def add_overlay(client: Client, message: Message, overlay_image_id, user_id):
    # Download the overlay image
    overlay_image = client.download_media(overlay_image_id)

    # Download the video
    video = client.download_media(message)

    # Read the video and overlay image
    cap = cv2.VideoCapture(video)
    overlay_img = cv2.imread(overlay_image)

    # Get the video dimensions and frame rate
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Resize the overlay image to match the video dimensions
    overlay_img = cv2.resize(overlay_img, (width, height))

    # Create a video writer to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use the original codec
    temp_output_path = os.path.join("/app", f"{user_id}.mp4")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (width, height))

    # Add the overlay to the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        overlayed_frame = cv2.addWeighted(frame, 0.8, overlay_img, 0.2, 0)  # Adjust blending weights
        out.write(overlayed_frame)

    # Release the video capture and writer
    cap.release()
    out.release()

    # Fix metadata using ffmpeg
    final_output_path = os.path.join("/app", f"{user_id}_fixed.mp4")
    fix_video_metadata(temp_output_path, final_output_path)

    # Send the output video
    client.send_video(message.chat.id, video=final_output_path)
