import ffmpeg
import requests
from PIL import Image
from io import BytesIO

def add_watermark(input_file, watermark_url):
    # Download the watermark image
    response = requests.get(watermark_url)
    img = Image.open(BytesIO(response.content))

    # Add the watermark to the video
    (
        ffmpeg
        .input(input_file)
        .overlay(img, x=10, y=10)
        .output('output.mp4')
        .run()
    )
