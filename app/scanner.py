from pprint import pprint
from uuid import uuid4
import nmap3
from app.database import Scanner_Data_Record, Vulnerability_Data_Record
from app.inventory import Inventory
from app.vulnerability.vulners_api import Vulnerability


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
        cve = Vulnerability(api_key="YK8IUSA59NZO8HYSKJEHT6WIZBOON2U64USK4VCFJGQAYIT0P0OEC0E72G1LFPDV")
        for inv_host in result_inventory:
            uuid = str(uuid4())
            result = nm.nmap_version_detection(inv_host)

            # pprint(result)

            for i in result:
                proto = i['protocol']
                port = i['port']
                state = i['state']
                product = None
                version = None
                name = None
                if 'service' in i:
                    if 'product' in i['service']:
                        product = i['service']['product']
                    else:
                        product = None
                    if 'version' in i['service']:
                        version = i['service']['version']
                    else:
                        version = None
                    if 'name' in i['service']:
                        name = i['service']['name']
                    else:
                        name = None
                # поиск cve и exploit
                if (product is not None) and (version is not None):
                    cve_search = cve.softwareVulnerabilities(name=product, version=version)
                    # pprint(cve_search)
                    for k in cve_search:
                        for j in k:
                            Vulnerability_Data_Record(data=j, name='softwareVulnerabilities',
                                                      task=uuid, port=port, port_name=name)
                    exploit_search = cve.publicExploits(name=product, version=version)
                    # pprint(exploit_search)
                    for u in exploit_search:
                        Vulnerability_Data_Record(data=u, name='publicExploits', task=uuid,
                                                  port=port, port_name=name)
                # брутфорс ssh
                if name == "ssh":
                    pass
                # брутфорс дирректорий web
                if name == "http" or name == "https":
                    pass
                # record in db
                Scanner_Data_Record(inv_host, proto, port, product, version, uuid, state, name)
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
