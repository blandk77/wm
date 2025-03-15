import os
from pyrogram import Client
from pyrogram.types import Message
import cv2
import numpy as np

def add_overlay(client: Client, message: Message, overlay_image_id, user_id):
    # Download the overlay image
    overlay_image = client.download_media(overlay_image_id)

    # Download the video
    video = client.download_media(message)

    # Read the video and overlay image
    cap = cv2.VideoCapture(video)
    overlay_img = cv2.imread(overlay_image)

    # Get the video dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Resize the overlay image to match the video dimensions
    overlay_img = cv2.resize(overlay_img, (width, height))

    # Create a video writer to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(os.path.join("/app", f"{user_id}.mp4"), fourcc, 30.0, (width, height))

    # Add the overlay to the video
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        overlayed_frame = cv2.addWeighted(frame, 1, overlay_img, 0.5, 0)
        out.write(overlayed_frame)

    # Release the video capture and writer
    cap.release()
    out.release()

    # Send the output video
    client.send_video(message.chat.id, video=os.path.join("/app", f"{user_id}.mp4"))
