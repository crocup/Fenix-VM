from abc import abstractmethod


class AbstractScanner:
    """
    """

    def __init__(self, host, db, table):
        self.host = host
        self.db = db
        self.table = table

    def template_scanner(self):
        result = self.scanner(self.host)
        new_result = self.del_misc_data(result)
        self.send_to_db(new_result)

    @abstractmethod
    def scanner(self, host):
        pass

    @abstractmethod
    def del_misc_data(self, data):
        pass

    @abstractmethod
    def send_to_db(self, result):
        pass


def result_scan(abstract_class: AbstractScanner):
    """
    """
    abstract_class.template_scanner()
