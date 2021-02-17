FROM python:3.8-buster

WORKDIR /ss-rando-bot

ENV QT_QPA_PLATFORM=offscreen

RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libxkbcommon-x11-0 \
  libdbus-1-3

COPY . .

RUN cd sslib && pip install -r requirements.txt

RUN pip install -e .