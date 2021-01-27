import datetime
from pprint import pprint
from uuid import uuid4
import nmap3
from app.database import Scanner_Data_Record, Inventory_Data_Filter_IP
from app.scanner.host_discovery import Inventory
from app.storage.database import Storage
from app.vulnerability.cve import CVE_MITRE


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
        inventory_service.result_host_discovery()

        for inv_host in result_inventory:
            result_json = dict()
            uuid = str(uuid4())
            result_json['uuid'] = uuid
            result_json['host'] = inv_host

            now = datetime.datetime.now()
            result_json['date'] = now.strftime("%d-%m-%Y %H:%M")

            tag_ip = Inventory_Data_Filter_IP(inv_host)
            result_json['tag'] = tag_ip['tag']

            result = nm.nmap_version_detection(inv_host)
            Scanner_Data_Record(inv_host, uuid)
            open_ports = []
            scann_port = result[inv_host]['ports']
            for i in scann_port:
                prt = dict()
                prt['port'] = i['portid']
                prt['protocol'] = i['protocol']
                prt['state'] = i['state']
                prt['name'] = None
                prt['product'] = None
                prt['version'] = None
                if 'service' in i:
                    if 'name' in i['service']:
                        prt['name'] = i['service']['name']
                        if 'product' in i['service']:
                            prt['product'] = i['service']['product']
                            if 'version' in i['service']:
                                prt['version'] = i['service']['version']
                # vulnerability cve mitre
                if prt['product'] is not None and prt['version'] is not None:
                    result_cve_mitre = CVE_MITRE(product=prt['product'], version=prt['version'])
                    prt['vulnerability'] = {'cve_mitre': result_cve_mitre.result_data()}

                open_ports.append(prt)
            result_json['open_port'] = open_ports
            # запись в базу данных
            scanner_data = Storage(db='scanner', collection='result')
            scanner_data.insert(data=result_json)
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
