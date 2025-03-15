# Telegram Video Overlay Bot

A Telegram bot that allows users to add a transparent image overlay (with text) to their videos.

## Features
- Add a custom transparent image overlay (with text) to videos.
- Supports videos up to 4GB.
- MongoDB integration for storing overlay images.

## Commands
- `/add`: Reply to a `.jpg` file to set it as your overlay image.
- `/remove`: Remove your overlay image from the database.

## Installation

1. Clone the repository:

bash
  git clone https://github.com/yourusername/telegram-video-overlay-bot.git
  cd telegram-video-overlay-bot

```

2. Install dependencies:
  
```

bash
  pip install -r requirements.txt

```

3. Add your configuration in config.py.

4. Run the bot:
  
```

bash
  python bot.py

```

▌Deployment
To deploy using Docker:
1. Build the Docker image:
  
```

bash
  docker build -t video-overlay-bot .

```

2. Run the container:
  
```

bash
  docker run -d video-overlay-bot

```

▌License
MIT

```
