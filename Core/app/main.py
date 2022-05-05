#!/usr/bin/venv python
import json
import os
import pika
import sys

from app.elk import send_elk


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="Core")

    def callback(ch, method, properties, body):
        result = json.loads(body)
        print(result)
        send_elk(doc=result)
    channel.basic_consume(queue="Core", on_message_callback=callback, auto_ack=True)
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
