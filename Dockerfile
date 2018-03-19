FROM python:3.4-alpine
MAINTAINER Edgar Felizmenio "edgarfelizmenio@gmail.com"

ADD . /code
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn