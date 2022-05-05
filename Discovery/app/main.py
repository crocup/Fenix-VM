#!/usr/bin/venv python
import json
import logging
import pika
import sys
from config import rabbit_mq
from discovery import result_scan, HostDiscovery


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbit_mq))
    channel = connection.channel()
    channel.queue_declare(queue="Discovery")

    def callback(ch, method, properties, body):
        result = json.loads(body)
        result_scan(HostDiscovery(host=result["host"]))

    channel.basic_consume(queue="Discovery", on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
        sys.exit(0)
