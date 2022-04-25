from abc import abstractmethod


class AbstractScanner:
    """
    """

    def __init__(self, host):
        self.host = host

    def template_scanner(self):
        result = self.scanner(self.host)
        data = self.del_misc_data(result)
        self.send_data(data)

    @abstractmethod
    def scanner(self, host):
        pass

    @abstractmethod
    def del_misc_data(self, data):
        pass

    @abstractmethod
    def send_data(self, result):
        pass


def result_scan(abstract_class: AbstractScanner):
    """
    """
    abstract_class.template_scanner()
