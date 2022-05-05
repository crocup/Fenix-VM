#!/usr/bin/venv python
import json
import logging
import pika
import sys
from config import rabbit_mq
from scanner import result_scan, HostScanner


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq))
    channel = connection.channel()
    channel.queue_declare(queue="Scanner")

    def callback(ch, method, properties, body):
        result = json.loads(body)
        result_scan(HostScanner(host=result["host"]))

    channel.basic_consume(queue="Scanner", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(0)
