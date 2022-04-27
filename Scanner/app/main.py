#!/usr/bin/venv python
import json
import pika, sys, os
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
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
