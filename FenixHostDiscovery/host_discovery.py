import datetime
from abc import abstractmethod
from typing import Dict, List
import nmap3
from database import MessageProducer, MongoDriver


class AbstractDiscovery:
    """

    """

    def __init__(self, host):
        self.nmap = nmap3.NmapHostDiscovery()
        self.host = host

    def template_discovery(self) -> Dict:
        return self.discovery(self.host)

    @abstractmethod
    def discovery(self, host):
        pass


class HostDiscovery(AbstractDiscovery):
    """Only host discover (-sn)"""

    def discovery(self, host) -> Dict:
        return self.nmap.nmap_no_portscan(host)


class ArpDiscovery(AbstractDiscovery):
    """Arp discovery on a local network (-PR)"""

    def discovery(self, host) -> Dict:
        return self.nmap.nmap_arp_discovery(host)


class PortScan(AbstractDiscovery):
    """Only port scan (-Pn)"""

    def discovery(self, host) -> Dict:
        return self.nmap.nmap_portscan_only(host)


def result_scanner(abstract_class: AbstractDiscovery):
    return abstract_class.template_discovery()


class DistributionDB:
    """

    """

    def __init__(self, host):
        self.host = host

    def template_db(self) -> Dict:
        """

        """
        response = result_scanner(HostDiscovery(self.host))
        result = self.delete_misc_data(response)
        list_data = self.edit_data_result(result)
        self.send_db(list_data)
        return dict(discovery='OK')

    def send_db(self, list_data: List):
        """

        """
        for data in list_data:
            message_host_discovery = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                                 base='Fenix', collection='HostDiscovery'))
            message_notification = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                               base='Fenix', collection='Notification'))
            data_ip = message_host_discovery.get_message({"host": str(data["host"])})
            if data_ip is None:
                message_host_discovery.insert_message(data)
                message_notification.insert_message({"time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                     "message": f"New IP: {data['host']}"})
            else:
                message_host_discovery.update_message(message={"host": data["host"]}, new_value=data)

    def edit_data_result(self, result):
        """

        """
        list_hostdiscovery = []
        for i in result:
            hostname = ""
            macaddress = ""
            if "hostname" in result[i]:
                hostname = result[i]["hostname"]
            if "macaddress" in result[i]:
                macaddress = result[i]["macaddress"]
            data = dict(host=i, hostname=hostname, macaddress=macaddress,
                        time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            list_hostdiscovery.append(data)
        return list_hostdiscovery

    def delete_misc_data(self, result: Dict) -> Dict:
        """

        """
        try:
            if "stats" in result:
                del result["stats"]
            if "runtime" in result:
                del result["runtime"]
        except Exception as e:
            result = {}
        return result
