import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip

def add_overlay(video_file, overlay_image):
    video = VideoFileClip(video_file)
    overlay = ImageClip(overlay_image).set_duration(video.duration)
    final_video = CompositeVideoClip([video, overlay])
    output_file = os.path.join(config.UPLOAD_DIR, "output.mp4")
    final_video.write_videofile(output_file)
    return output_file
