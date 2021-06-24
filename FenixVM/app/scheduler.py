"""
Scheduler
Автоматический запуск задач на обнаружение
и сканирование важных хостов в сети.
Задачи запускаются в фоне с помощью RQ Worker
Dmitry Livanov, 2021
"""
from app.config import *
from app.service.database import MessageProducer, MongoDriver
from app.task import host_discovery_task, scan_task


class Scheduler:
    pass


def scheduler_host_discovery():
    """
    Запуск задачи на обнаружение хостов в сети.
    Поиск хостов осуществляется каждые 5 минут
    :return: None
    """
    setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                               base="setting", collection="network"))
    items = setting_data.get_all_message()
    for net in items:
        host_discovery_task(host=net["network"])


def scheduler_scanner():
    """
    Запуск задачи на сканирвоние важных хостов.
    Важные хосты настраиваются на вкладке Host Discovery -> <ip> -> Edit Host
    Сканирование осуществляется каждые 24 часа.
    :return: None
    """
    host_discovery = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                 base="FenixHostDiscovery", collection="result"))
    items = host_discovery.get_all_message()
    list_ip = []
    for data in items:
        if data["important"]:
            list_ip.append(data["ip"])
    for net in list_ip:
        scan_task(net)
