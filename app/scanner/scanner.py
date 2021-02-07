import datetime
from pprint import pprint
from uuid import uuid4
# from app.database import Scanner_Data_Record
from app.scanner.host_discovery import *
from app.storage.database import Storage
from app.vulnerability.cve import CVE_MITRE


class Scanner:
    def __init__(self, host):
        """

        :param host:
        """
        self.host = host

    def scan_service_version(self, host):
        """

        :return:
        """
        nm = nmap3.Nmap()
        return nm.nmap_version_detection(host)

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

    def scanner_task(self, host):
        """

        :param host:
        :return:
        """
        result_json = dict()
        open_ports = []
        uuid = str(uuid4())
        result_json['uuid'] = uuid
        result_json['host'] = host

        now = datetime.datetime.now()
        result_json['date'] = now.strftime("%d-%m-%Y %H:%M")

        host_discovery_tag = Storage(db='host_discovery', collection='result')
        tag_ip = host_discovery_tag.get_one({"ip": host})
        for tags in tag_ip:
            result_json['tag'] = tags['tag']

        result = self.scan_service_version(host)
        # Scanner_Data_Record(host, uuid)

        scann_port = result[host]['ports']
        for i in scann_port:
            prt = dict()
            prt['port'] = i['portid']
            prt['protocol'] = i['protocol']
            prt['state'] = i['state']
            prt['name'] = None
            prt['product'] = None
            prt['version'] = None
            prt['vulnerability'] = {'cve_mitre': []}
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
