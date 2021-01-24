import datetime
from pprint import pprint
from uuid import uuid4
import nmap3
from app import db_scanner
from app.database import Scanner_Data_Record, Inventory_Data_Filter_IP
from app.inventory import Inventory
from app.vulnerability import cve
from app.vulnerability.cve import cve_mitre


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
            result_json = {}
            uuid = str(uuid4())
            result = nm.nmap_version_detection(inv_host)
            result_json['scanner'] = result
            Scanner_Data_Record(inv_host, uuid)

            for scanner_vulnerability in result_json['scanner']:
                # print(scanner_vulnerability)
                if 'service' in scanner_vulnerability:
                    # print(scanner_vulnerability["service"])
                    if 'product' in scanner_vulnerability["service"]:
                        product = scanner_vulnerability["service"]["product"]
                    else:
                        product = None
                    if 'version' in scanner_vulnerability["service"]:
                        version = scanner_vulnerability["service"]["version"]
                    else:
                        version = None
                    mitre = cve_mitre(product=product, version=version)
                    res = mitre.search()
                    mitre_cve_array = []
                    if res is not None:
                        for list_cve in res['cve_mitre']:
                            result = cve.find_cve(list_cve)
                            mitre_cve_list = {'cve': list_cve,
                                              'value': result['value'],
                                              'CVSS Score': result['impact']['baseMetricV2']['cvssV2']['baseScore']
                                              }
                            mitre_cve_array.append(mitre_cve_list)

                    scanner_vulnerability['vulnerability'] = {'cve_mitre': mitre_cve_array}
                    # print(mitre_cve_array)

            result_json['uuid'] = uuid
            result_json['host'] = inv_host
            now = datetime.datetime.now()
            result_json['date'] = now.strftime("%d-%m-%Y %H:%M")
            posts = db_scanner['result']
            tag_ip = Inventory_Data_Filter_IP(inv_host)
            result_json['tag'] = tag_ip['tag']
            posts.insert(result_json)
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
