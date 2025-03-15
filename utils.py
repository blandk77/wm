import os
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

def add_overlay(message, overlay_image):
    video_file = message.download()
    overlay_file = f"{overlay_image}.jpg"
    client.download_media(overlay_image, file_name=overlay_file)
    video = VideoFileClip(video_file)
    overlay = ImageClip(overlay_file).set_duration(video.duration)
    final_video = CompositeVideoClip([video, overlay])
    output_file = os.path.join(config.UPLOAD_DIR, "output.mp4")
    final_video.write_videofile(output_file)
    return output_file
