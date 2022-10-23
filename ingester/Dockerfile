FROM python:latest

WORKDIR /ingester

RUN apt-get update
RUN apt-get install ffmpeg -y

RUN pip install \
    celery[redis] \
    elasticsearch \
    pytube \
    git+https://github.com/openai/whisper.git