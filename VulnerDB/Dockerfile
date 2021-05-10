FROM python:3.8-alpine

MAINTAINER Dmitry Livanov "[patunutap@gmail.com]"

RUN apt update -y && \
    apt upgrade -y

WORKDIR /usr/src/vulnerdb

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "vulnerdb-module.py"]