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


def scan_db_task(result: str, host: str):
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
    requests.post(API_DATABASE + '/insert', json={"data": data,
                                                  "base": "scanner", "collection": "task"})


def host_discovery_task(host: str):
    """
    Запуск задачи по обнаружению хостов в сети
    Используется микросервис
    :param host:
    :return:
    """
    try:
        result = requests.post(HOST_DISCOVERY, json={"host": host})
        print(result.json())
    except Exception as e:
        print(e)
