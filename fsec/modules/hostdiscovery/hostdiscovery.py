import datetime
from abc import abstractmethod
from typing import Dict, List
import nmap3


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


def arp_scan_data(data):
    return result_scanner(HostDiscovery(data))


def arp_scan(data):
    response = result_scanner(HostDiscovery(data))
    response = delete_misc_data(response)
    hostname = ""
    macaddress = ""
    host = ""
    time = ""
    for i in response:
        host = i
        print(i)
        if "hostname" in response[i]:
            hostname = response[i]["hostname"]
        if "macaddress" in response[i]:
            macaddress = response[i]["macaddress"]
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return host, str(hostname), str(macaddress), time


def delete_misc_data(result: Dict) -> Dict:
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
