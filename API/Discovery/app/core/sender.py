from abc import abstractmethod


class AbstractSender:
    """
    """

    def __init__(self, data):
        self.data = data

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
