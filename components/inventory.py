import ipaddress
import os
import scapy.all
import socket
from components.record_database import RecordMongo
import configparser
import datetime

# read setting file
path = "settings/settings.conf"
config = configparser.ConfigParser()
config.read(path)


def record_in_mongo(result_inventory, now_time):
    """

    """
    record_mongo = RecordMongo(db=config.get("DATABASE_INVENTORY", "BASE"),
                               coll=config.get("DATABASE_INVENTORY", "COLLECTION"))
    record_mongo.database_inventory(result=result_inventory, date_now=now_time)
    record_mongo.close_connection()


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
        arp_request = scapy.all.ARP(pdst=self.target)
        broadcast = scapy.all.Ether(dst='ff:ff:ff:ff:ff:ff')
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.all.srp(arp_request_broadcast, timeout=3, verbose=False)[0]
        clients_list = []
        for element in answered_list:
            clients_list.append(element[1].psrc)
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
            # return list(set(self.scan_arp() + self.ping_scan()))
            result = list(set(self.scan_arp()))
            now_time = datetime.datetime.now()
            record_in_mongo(result, now_time)
            status = "success"
            return status
        except Exception as e:
            status = "error: {}".format(e)
            return status

    def my_ip(self):
        """

        :return:
        """
        return (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                  if not ip.startswith("127.")]
                 or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close())
                      for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
