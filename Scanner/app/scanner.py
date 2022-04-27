import datetime
import json
import logging
from abc import abstractmethod
from typing import Dict
import nmap3

from sender import result_sender, HostSenderData


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


class HostScanner(AbstractScanner):
    """Only host discover (-sn)"""

    def scanner(self, host) -> Dict:
        """
        """
        return nmap3.Nmap().nmap_version_detection(host)

    def del_misc_data(self, data) -> Dict:
        """
        """
        try:
            if "stats" in data:
                del data["stats"]
            if "runtime" in data:
                del data["runtime"]
        except Exception as e:
            data = {}
            logging.error(e)
        return data

    def send_data(self, result):
        try:
            """
            отправка в брокер сообщений
            """
            for host in result:
                # send to rabbitmq
                result_data = {
                    "service": "scanner",
                    "host_addr": host,
                    "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "data": result[host]
                }
                result_sender(HostSenderData(data=json.dumps(result_data), rabbit_queue="Core"))
        except Exception as e:
            logging.error(e)
