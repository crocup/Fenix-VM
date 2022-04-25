import pika
from API.Discovery.app.core.config import settings
from API.Discovery.app.core.sender import AbstractSender


class HostSenderData(AbstractSender):

    def __init__(self, data):
        super().__init__(data)
        self.channels = None
        self.connections = None
        self.host = settings.RABBITMQ
        self.queue = settings.RABBITMQ_QUEUE
        self.routing_key = settings.RABBITMQ_KEY

    def connect(self):
        self.connections = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channels = self.connections.channel()
        self.channels.queue_declare(queue=self.queue)

    def send_data(self, data):
        self.channels.basic_publish(exchange='', routing_key=self.routing_key, body=data)

    def disconnect(self):
        self.connections.close()
