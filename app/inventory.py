import ipaddress
import os
from scapy.all import srp, Ether, ARP, conf
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

    def __init__(self, target, interface):
        """

        :param target: ip address/mask network (example 192.168.100.0/24)
        """
        self.target = target
        self.interface = interface

    def scan_arp(self):
        """

        :return: list ip address and mac
        """
        try:
            clients_list = []
            conf.verb = 0
            pkt = Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=self.target)
            ans, unans = srp(pkt, iface=self.interface, timeout=2, verbose=False, inter=0.1)
            for snt, recv in ans:
                if recv:
                    clients_list.append(recv[ARP].psrc)
        except Exception:
            clients_list = []
        return clients_list

    def ping_scan(self):
        """
        :return:
        """
        result = []
        ip_net = ipaddress.ip_network(self.target)
        all_hosts = list(ip_net.hosts())
        for hostname in range(len(all_hosts)):
            response = os.system("ping -c1 -w1 " + str(all_hosts[hostname]))
            if response == 0:
                result.append(str(all_hosts[hostname]))
        return result

    def result_scan(self):
        """

        :return:
        """
        try:
            result = list(self.ping_scan()+self.scan_arp())
            record_db(result)
            return "success"
        except Exception as e:
            status = "error: {}".format(e)
            return status

    def result_scan_arp(self):
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
