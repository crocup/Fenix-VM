from abc import abstractmethod
from typing import Dict
import nmap3
from fsec.database import MessageProducer, MongoDriver
from datetime import datetime


class AbstractDiscovery:
    """
    """

    def __init__(self, host):
        self.nmap = nmap3.NmapHostDiscovery()
        self.host = host

    def template_discovery(self):
        result = self.discovery(self.host)
        new_result = self.del_misc_data(data=result)
        self.send_to_db(new_result)

    @abstractmethod
    def discovery(self, host):
        pass

    @abstractmethod
    def del_misc_data(self, data):
        pass

    @abstractmethod
    def send_to_db(self, result):
        pass


class HostDiscovery(AbstractDiscovery):
    """Only host discover (-sn)"""

    def discovery(self, host) -> Dict:
        """

        """
        return self.nmap.nmap_no_portscan(host)

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
        return data

    def send_to_db(self, result):
        """

        """
        message_host_discovery = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                             base='HostDiscovery', collection='result'))
        for host in result:
            data = {
                "host": host,
                "hostname": result[host]["hostname"],
                "macaddress": result[host]["macaddress"],
                "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")
            }
            data_ip = message_host_discovery.get_message({"host": str(host)})
            if data_ip is None:
                message_host_discovery.insert_message(data)
            else:
                message_host_discovery.update_message(message={"host": host},
                                                      new_value={"macaddress": result[host]["macaddress"],
                                                                 "hostname": result[host]["hostname"],
                                                                 "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")})


def result_scanner(abstract_class: AbstractDiscovery):
    """

    """
    abstract_class.template_discovery()

