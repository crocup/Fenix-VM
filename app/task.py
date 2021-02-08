from app import time
from app.config import HOST_DISCOVERY
from app.service.scanner.scanner import Scanner
from app.storage.database import Storage
from app.service.inventory.api import *
import requests


def scan_task(network_mask: str) -> str:
    """

    :param network_mask:
    :return:
    """
    scanner = Scanner(network_mask)
    result_inventory = scan_arp(target=network_mask)
    for host in result_inventory:
        scanner.scanner_task(host)
    return "success"


def scan_db_task(result, host):
    """

    :param result:
    :param host:
    :return:
    """
    # запись в БД task
    task_ip = Storage(db='scanner', collection='task')
    data = {
        "uuid": result,
        "name": "Scanner",
        "host": host,
        "time": time()
    }
    task_ip.insert(data=data)


def host_discovery_task(host: str):
    """

    :param host:
    :return:
    """
    try:
        result = requests.post(HOST_DISCOVERY, json={"host": host})
        data = result.json()
        # запись результата в базу данных
        host_discovery_data = Storage(db='host_discovery', collection='result')
        for host_discovery in data["data"]:
            data_ip = host_discovery_data.get_one({"ip": host_discovery})
            if data_ip.count() == 0:
                host_discovery_data.insert({"ip": host_discovery, "tag": None, "time": time()})
                # оповещение (запись в mongo)
                notifications_data = Storage(db='notification', collection='notifications')
                notifications_data.insert({"time": time(), "message": f"New IP: {host_discovery}"})
            else:
                host_discovery_data.upsert({"ip": host_discovery}, {"time": time()})
        return "success"
    except Exception:
        return "error"
