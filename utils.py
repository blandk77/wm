import os
import ffmpeg
from moviepy import VideoFileClip, ImageClip, CompositeVideoClip

def add_overlay(client, message, overlay_image):
    video_file = message.download()
    overlay_file = f"overlay_{overlay_image}.jpg"
    client.download_media(overlay_image, file_name=overlay_file)
    
    # Get the video duration
    video_duration = ffmpeg.probe(video_file)['format']['duration']
    
    # Create the overlay clip
    overlay = ImageClip(overlay_file).set_duration(float(video_duration)).resize((1920,1080))
    
    # Create the video clip
    video = VideoFileClip(video_file)
    
    # Create the final clip with the overlay
    final_clip = CompositeVideoClip([video, overlay.set_position('center')], size=video.size)
    
    # Write the final clip to a new video file
    output_file = os.path.join("uploads", "output.mkv")
    final_clip.write_videofile(output_file, codec="copy")
    
    return output_file
