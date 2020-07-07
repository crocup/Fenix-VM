import nmap3
from . import time
from .models import InventoryPost, db


def record_db(result_inventory):
    """

    :param result_inventory:
    :return:
    """
    for res in result_inventory:
        ips_find = InventoryPost.query.filter_by(ip=res).first()
        if ips_find is None:
            reg = InventoryPost(res, time())
            db.session.add(reg)
        else:
            ips_find.dateofreg = time()
            db.session.add(ips_find)
    db.session.commit()


def data_delete(ip):
    """

    :param ip:
    :return:
    """
    InventoryPost.query.filter_by(ip=ip).delete()
    db.session.commit()


class Inventory(object):

    def __init__(self, target):
        """

        :param target: ip address/mask network (example 192.168.100.0/24)
        """
        self.target = target

    def scan_arp(self):
        """

        :return: list ip address and mac
        """
        try:
            clients_list = []
            hd_scan = nmap3.NmapHostDiscovery()
            result = hd_scan.nmap_no_portscan(self.target)
            for res in result['hosts']:
                addr = res['addr']
                clients_list.append(addr)
        except Exception as e:
            clients_list = []
        return clients_list

    def result_scan(self):
        """

        :return:
        """
        try:
            result = list(self.scan_arp())
            record_db(result)
            return "success"
        except Exception as e:
            status = "error: {}".format(e)
            return status
