import datetime
from pprint import pprint
from uuid import uuid4

import requests
from nmap3 import nmap3

from app.config import DATABASE
from app.plugins.vulnerability import result_code, VulnDB, CveMitre
from app.service.database_old.database import Storage


def scanner_uuid(host):
    result_json = dict()
    uuid = str(uuid4())
    result_json['host'] = host
    result_json['uuid'] = uuid
    now = datetime.datetime.now()
    result_json['date'] = now.strftime("%d-%m-%Y %H:%M")
    host_discovery_tag = Storage(db='host_discovery', collection='result')
    tag_ip = host_discovery_tag.data_one({"ip": host})
    for tags in tag_ip:
        result_json['tag'] = tags['tag']
    scanner_data = Storage(db='scanner', collection='result')
    scanner_data.insert(data=result_json)
    return uuid


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
        uuid = scanner_uuid(host=host)
        result = self.scan_service_version(host)
        scann_port = result[host]['ports']
        for i in scann_port:
            prt = dict()
            prt['port'] = i['portid']
            prt['protocol'] = i['protocol']
            prt['state'] = i['state']
            prt['name'] = None
            prt['product'] = None
            prt['version'] = None
            if 'cpe' in i:
                for cpe_data in i['cpe']:
                    prt['cpe'] = cpe_data['cpe']
            prt['plugins'] = {'cve_mitre': []}
            if 'service' in i:
                if 'name' in i['service']:
                    prt['name'] = i['service']['name']
                    if 'product' in i['service']:
                        prt['product'] = i['service']['product']
                        if 'version' in i['service']:
                            prt['version'] = i['service']['version']
            if prt['product'] is not None and prt['version'] is not None:
                result_cvemitre = result_code(CveMitre(), product=prt['product'], version=prt['version'])
                prt['plugins'] = {'cve_mitre': result_cvemitre['data']}
            open_ports.append(prt)
        result_json['open_port'] = open_ports
        # запись в базу данных
        # scanner_data = Storage(db='scanner', collection='result')
        # scanner_data.upsert(name={"uuid": uuid}, data=result_json)
        data = {"uuid": uuid}
        requests.post(DATABASE + '/upsert', json={"data": data, "set": result_json,
                                                  "base": "scanner", "collection": "result"})
