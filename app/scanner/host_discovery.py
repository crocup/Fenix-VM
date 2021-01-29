import re
import nmap3
from app.database import Inventory_Data_Delete


def delete_ip(host):
    try:
        Inventory_Data_Delete(host)
    except Exception as e:
        print(f"error: {e}")


def scan_arp(target):
    """

    :return: list ip address and mac
    """
    try:
        clients_list = []
        hd_scan = nmap3.NmapHostDiscovery()
        result = hd_scan.nmap_no_portscan(target)
        for res in result:
            check_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res)
            if check_ip:
                ip = check_ip.group()
                clients_list.append(ip)
    except Exception:
        clients_list = []
    return clients_list
