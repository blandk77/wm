import os
from moviepy.editor import VideoFileClip, CompositeVideoClip, ImageClip

def add_overlay(video_path, overlay_image_path, output_path):
    """
    Adds a transparent image overlay to a video and saves the output.

    Args:
        video_path (str): Path to the input video.
        overlay_image_path (str): Path to the overlay image.
        output_path (str): Path to save the processed video.

    Returns:
        str: Path to the processed video.
    """
    try:
        # Load the video
        video = VideoFileClip(video_path)

        # Create an image overlay
        overlay_image = ImageClip(overlay_image_path).set_duration(video.duration).set_position(("center", "top")).resize(height=100)

        # Combine video with overlay
        final_video = CompositeVideoClip([video, overlay_image])

        # Write the output file
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")

        return output_path
    except Exception as e:
        raise RuntimeError(f"Error processing video: {e}")

def ensure_temp_dir_exists(temp_dir):
    """
    Ensures the temporary directory exists.
    """
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
