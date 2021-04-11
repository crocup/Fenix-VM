from time import sleep
from app import time
from app.config import *
from app.service.scanner.scanner import Scanner
import requests


def scan_task(network_mask: str) -> str:
    """
    Запуск задачи сканирвоания
    :param network_mask:
    :return:
    """
    scanner = Scanner(network_mask)
    task_id = requests.post(f"{HOST_DISCOVERY}/get", json={"host": network_mask})
    task = task_id.json()
    while True:
        sleep(3)
        result_discovery = requests.get(f"{HOST_DISCOVERY}/results/{task['job']}")
        if result_discovery.status_code == 200:
            break
    ret = eval(result_discovery.content.decode())
    for host in ret['result']:
        scanner.scanner_task(host)
    return "success"


def scan_db_task(result: str, host: str):
    """
    Запись в БД
    :param result:
    :param host:
    :return:
    """
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
        requests.post(f"{HOST_DISCOVERY}/get", json={"host": host})
    except Exception as e:
        print(e)


def delete_data_host_discovery(host: str):
    """

    """
    try:
        requests.post(f"{DATABASE}/delete", json={"data": {"ip": host},
                                                  "base": "host_discovery", "collection": "result"})
        requests.post(f"{DATABASE}/delete", json={"data": {"host": host},
                                                  "base": "scanner", "collection": "result"})
        requests.post(f"{DATABASE}/delete", json={"data": {"host": host},
                                                  "base": "scanner", "collection": "task"})
    except Exception as e:
        print(e)
