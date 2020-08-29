from pprint import pprint
from uuid import uuid4
import nmap3
from app.database import record_scan
from app.inventory import Inventory


class Scanner:
    """

    """

    def __init__(self, host):
        """

        :param host:
        """
        self.host = host

    def scan_service_version(self):
        """

        :return:
        """
        nm = nmap3.Nmap()
        inventory_service = Inventory(target=self.host)
        result_inventory = inventory_service.scan_arp()
        inventory_service.result_scan()
        for inv_host in result_inventory:
            uuid = str(uuid4())
            result = nm.nmap_version_detection(inv_host)
            for i in result:
                proto = i['protocol']
                port = i['port']
                if 'service' in i:
                    if 'product' in i['service']:
                        product = i['service']['product']
                    else:
                        product = None
                    if 'version' in i['service']:
                        version = i['service']['version']
                    else:
                        version = None
                else:
                    product = None
                    version = None
                record_scan(inv_host, proto, port, product, version, uuid)
        return "success"

    def scan_arp(self):
        """

        :return:
        """
        arp_nmap = nmap3.NmapHostDiscovery()
        result = arp_nmap.nmap_arp_discovery(self.host)
        pprint(result)

    def scan_ping(self):
        """

        :return:
        """
        nm_ping = nmap3.NmapScanTechniques()
        return nm_ping.nmap_ping_scan(self.host)

    def scan_subnet(self):
        """

        :return:
        """
        nm = nmap3.Nmap()
        return nm.nmap_subnet_scan(self.host)
