from time import sleep
import requests
from scanner_new import result_scanner, ScannerTask
import conf


def scanner_work(network_mask: str) -> str:
    """
    Запуск задачи сканирвоания
    :param network_mask:
    :return:
    """
    task_id = requests.post(f"{conf.Config.HOST_DISCOVERY}/get", json={"host": network_mask})
    task = task_id.json()
    while True:
        sleep(3)
        result_discovery = requests.get(f"{conf.Config.HOST_DISCOVERY}/results/{task['job']}")
        if result_discovery.status_code == 200:
            break
    ret = eval(result_discovery.content.decode())
    for host in ret['result']:
        result_scanner(ScannerTask(host))
    return "success"
