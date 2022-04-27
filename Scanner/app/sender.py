from abc import abstractmethod
import pika
from config import rabbit_mq


class AbstractSender:
    """
    """

    def __init__(self, data, rabbit_queue):
        self.data = data
        self.host = rabbit_mq
        self.queue = rabbit_queue
        self.routing_key = rabbit_queue
        self.channels = None
        self.connections = None

    def template_sender(self):
        self.connect()
        self.send_data(self.data)
        self.disconnect()

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def send_data(self, data):
        pass

    @abstractmethod
    def disconnect(self):
        pass


def result_sender(abstract_class: AbstractSender):
    """
    """
    abstract_class.template_sender()


class HostSenderData(AbstractSender):

    def connect(self):
        self.connections = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        self.channels = self.connections.channel()
        self.channels.queue_declare(queue=self.queue)

    def send_data(self, data):
        self.channels.basic_publish(exchange='', routing_key=self.routing_key, body=data)

    def disconnect(self):
        self.connections.close()
