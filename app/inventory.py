import nmap3
from app.database import Inventory_Data_Record


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
            Inventory_Data_Record(result)
            return "success"
        except Exception as e:
            status = "error: {}".format(e)
            return status
