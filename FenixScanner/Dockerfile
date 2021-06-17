FROM python:3.8-alpine

MAINTAINER Dmitry8925 "[patunutap@gmail.com]"

RUN apt update -y && \
    apt upgrade -y

WORKDIR /usr/src/fenix_scan

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]