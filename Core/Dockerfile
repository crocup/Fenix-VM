FROM python:3.9
MAINTAINER info@fsec.com
RUN apt-get update && apt-get install -y nmap
RUN pip install --upgrade pip
# install app
WORKDIR /Scanner
COPY ./requirements.txt /Scanner/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /Scanner/requirements.txt
COPY ./app /Scanner
CMD ["python", "main.py"]
