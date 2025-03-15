#Telegram Bot for Adding Image Overlays to Videos

This is a Telegram bot that allows users to add image overlays to videos. The bot uses the Pyrogram library to interact with the Telegram API and the MoviePy library to edit videos.

Features
```
- Add image overlays to videos
- Remove image overlays from videos
- Store overlay images in a MongoDB database
- Support for video and document files
```
Requirements
```
- Python 3.9+
- Pyrogram library
- MoviePy library
- MongoDB
- Docker
```
Installation
1. Clone the repository using `git clone https://github.com/blandk77/wm.git`
2. Create a new directory for the project and navigate into it
3. Copy the `config.py.example` file to `config.py` and fill in your Telegram API credentials, MongoDB credentials, and other settings
4. Build the Docker image using `docker build -t telegram-bot .`
5. Run the Docker container using `docker run -d --name telegram-bot telegram-bot`

Usage
1. Start the bot by sending the `/start` command
2. Add an image overlay to a video by sending the `/add` command and replying to the video message with the image
3. Remove an image overlay from a video by sending the `/remove` command and replying to the video message with the image
4. The bot will process the video and send the output back to the user

Contributing
Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
This project uses the following libraries and services:

- Pyrogram: A Python library for the Telegram API
- MoviePy: A Python library for video editing
- MongoDB: A NoSQL database service
- Docker: A containerization platform
