import ffmpeg
from PIL import Image

def add_watermark(input_file, watermark_url):
    # Download the watermark image
    watermark_image = Image.open(watermark_url)

    # Add the watermark to the video
    (
        ffmpeg
        .input(input_file)
        .overlay(watermark_image, x=10, y=10)
        .output('output.mp4')
        .run()
    )
