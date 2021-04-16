"""
Scheduler
Автоматический запуск задач на обнаружение
и сканирование важных хостов в сети.
Задачи запускаются в фоне с помощью RQ Worker
Dmitry Livanov, 2021
"""
from app.main import q
from app.service.database_old.database import Storage
from app.task import host_discovery_task, scan_task, scan_db_task


def scheduler_host_discovery():
    """
    Запуск задачи на обнаружение хостов в сети.
    Поиск хостов осуществляется каждые 5 минут
    :return: None
    """
    setting_data = Storage(db='setting', collection='network')
    items = setting_data.find_data_all()
    for net in items:
        q.enqueue_call(host_discovery_task, args=(net["network"],), result_ttl=500)


def scheduler_scanner():
    """
    Запуск задачи на сканирвоние важных хостов.
    Важные хосты настраиваются на вкладке Host Discovery -> <ip> -> Edit Host
    Сканирование осуществляется каждые 24 часа.
    :return: None
    """
    host_discovery = Storage(db='host_discovery', collection='result')
    items = host_discovery.find_data_all()
    list_ip = []
    for data in items:
        if data["important"]:
            list_ip.append(data["ip"])
    for net in list_ip:
        results = q.enqueue_call(scan_task, args=(net,), result_ttl=500)
        scan_db_task(result=results.id, host=net)
