FROM python:3.10.4

WORKDIR /app

COPY ./app /app

RUN apt-get update
RUN apt-get install -y vim
RUN apt-get install -y ffmpeg

RUN pip install Flask
RUN pip install pydub
RUN pip install ffmpeg-python

RUN python --version

CMD python index.py

