FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

EXPOSE 8000

CMD gunicorn app:app & python main.py
