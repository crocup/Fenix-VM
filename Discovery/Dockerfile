FROM python:3.9
MAINTAINER info@fsec.com
RUN apt-get update && apt-get install -y nmap
RUN pip install --upgrade pip
# install app
WORKDIR /Discovery
COPY ./requirements.txt /Discovery/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /Discovery/requirements.txt
COPY ./app /Discovery
CMD ["python", "main.py"]
