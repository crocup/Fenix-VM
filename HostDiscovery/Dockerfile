FROM python:3.8-alpine

MAINTAINER Dmitry Livanov "[patunutap@gmail.com]"

RUN apt update -y && \
    apt upgrade -y

WORKDIR /usr/src/hostdiscovery

COPY . .

RUN pip install -r requirements.txt

EXPOSE 9001

ENTRYPOINT ["python", "worker.py"]

ENTRYPOINT ["python", "app.py"]