import ipaddress
import os
import scapy.all
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


def all_data():
    ary = []
    all_ip = InventoryPost.query.all()
    for u in all_ip:
        lists = [u.ip, u.name, u.dateofreg]
        ary.append(lists)
    # print(ary)
    return ary


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
            arp_request = scapy.all.ARP(pdst=self.target)
            broadcast = scapy.all.Ether(dst='ff:ff:ff:ff:ff:ff')
            arp_request_broadcast = broadcast / arp_request
            answered_list = scapy.all.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
            clients_list = []
            for element in answered_list:
                clients_list.append(element[1].psrc)
        except Exception as e:
            print(e)
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

        :param ping: True/False
        :return:
        """
        try:
            result = list(set(self.ping_scan()+self.scan_arp()))
            record_db(result)
            status = "success"
            return status, result
        except Exception as e:
            status = "error: {}".format(e)
            return status
