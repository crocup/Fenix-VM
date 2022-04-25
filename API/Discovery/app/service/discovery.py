import logging
from datetime import datetime
from typing import Dict
import nmap3
from API.Discovery.app.core.scanner import AbstractScanner
from API.Discovery.app.core.sender import result_sender
from API.Discovery.app.models.model import DiscoveryMessage
from API.Discovery.app.service.sender import HostSenderData


class HostDiscovery(AbstractScanner):
    """Only host discover (-sn)"""

    def scanner(self, host) -> Dict:
        """
        """
        return nmap3.NmapHostDiscovery().nmap_no_portscan(host)

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
                mac = "None"
                if result[host]['macaddress'] is not None:
                    mac = result[host]['macaddress']['addr']
                # send to rabbitmq
                result_data = DiscoveryMessage(service="Discovery", host=host, mac_addr=mac,
                                               time="time")
                result_sender(HostSenderData(data=result_data.json()))
        except Exception as e:
            logging.error(e)
