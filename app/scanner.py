from pprint import pprint
from uuid import uuid4
import nmap3
from app import time, db
from app.models import InventoryPost, ScannerPost
from app.inventory import Inventory


def group_by(uid):
    try:
        dictionary = {}
        r = ScannerPost.query.filter(ScannerPost.uuid == str(uid))
        for i in r:
            dictionary['ip'] = i.ip
            dictionary['port'] = i.port
            dictionary['dateofreg'] = i.dateofreg
            dictionary['uuid'] = uid
            print(dictionary)
        return dictionary
    except Exception as e:
        print(e)
        return {}


def group_ip_date():
    return db.session.query(ScannerPost.ip, ScannerPost.dateofreg, ScannerPost.uuid).group_by(ScannerPost.uuid).all()


def record_scan(host, proto, port, product, version, uuid):
    """

    :param host:
    :param proto:
    :param port:
    :param product:
    :param version:
    :return:
    """
    some_owner = InventoryPost.query.filter_by(ip=host).first()
    scanford = ScannerPost(protocol=proto, port=port, service_name=product, service_version=version,
                           dateofreg=time(), owner=some_owner, ip=host, uuid=uuid)
    db.session.add(scanford)
    db.session.commit()


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
        print(result_inventory)
        for inv_host in result_inventory:
            uuid = str(uuid4())
            print(uuid)
            result = nm.nmap_version_detection(inv_host)
            print(result)
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
