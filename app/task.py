from app import time
from app.config import *
from app.notification import telegram_message
from app.service.scanner.scanner import Scanner
import requests


def scan_task(network_mask: str) -> str:
    """

    :param network_mask:
    :return:
    """
    scanner = Scanner(network_mask)
    result_inventory = requests.post(HOST_DISCOVERY, json={"host": network_mask})
    data = result_inventory.json()
    for host in data["data"]:
        scanner.scanner_task(host)
    return "success"


def scan_db_task(result, host):
    """

    :param result:
    :param host:
    :return:
    """
    # запись в БД task
    data = {
        "uuid": result,
        "name": "Scanner",
        "host": host,
        "time": time()
    }
    requests.post(INSERT_DATABASE, json={"data": data,
                                         "base": "scanner", "collection": "task"})


def host_discovery_task(host: str):
    """

    :param host:
    :return:
    """
    try:
        result = requests.post(HOST_DISCOVERY, json={"host": host})
        data = result.json()
        # запись результата в базу данных
        for host_discovery in data["data"]:
            data_ip = requests.post(GET_ONE_DATABASE, json={"data": {"ip": host_discovery},
                                                            "base": "host_discovery", "collection": "result"})
            data_ip = data_ip.json()
            if len(data_ip['data']) == 0:
                requests.post(INSERT_DATABASE, json={"data": {"ip": host_discovery, "tag": None, "time": time()},
                                                     "base": "host_discovery", "collection": "result"})
                # оповещение
                message = f"New IP: {host_discovery}"
                requests.post(INSERT_DATABASE, json={"data": {"time": time(), "message": message},
                                                     "base": "notification", "collection": "notifications"})
                # оповещение в телеграм
                telegram_message(message)
            else:
                requests.post(UPSERT_DATABASE, json={"data": {"name": {"ip": host_discovery}, "set": {"time": time()}},
                                                     "base": "host_discovery", "collection": "result"})
        return "success"
    except Exception as e:
        return "error"
