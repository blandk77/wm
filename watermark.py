import cv2
import numpy as np
import ffmpeg
import requests

def add_watermark(input_file, watermark_url):
    # Download the watermark image
    response = requests.get(watermark_url)
    nparr = np.frombuffer(response.content, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Save the image to a temporary file
    cv2.imwrite('watermark.png', img)

    # Add the watermark to the video
    (
        ffmpeg
        .input(input_file)
        .overlay(ffmpeg.input('watermark.png'), x=10, y=10)
        .output('output.mp4')
        .run()
    )
