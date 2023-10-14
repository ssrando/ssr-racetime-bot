FROM python:3.10-alpine

WORKDIR /ss-rando-bot

RUN apk add git

COPY setup.py .
COPY randobot randobot

RUN pip install -e .