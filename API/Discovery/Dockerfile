FROM python:3.9
MAINTAINER info@fsec.com
RUN apt-get update && apt-get install -y supervisor nmap
RUN pip install --upgrade pip
RUN mkdir -p /var/log/supervisor
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
# install app
WORKDIR /API/Discovery
COPY ./requirements.txt /API/Discovery/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /Discovery/requirements.txt
COPY ./app /API/Discovery/app

CMD ["/usr/bin/supervisord"]
