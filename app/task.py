from app import time
from app.storage.database import Storage
from app.scanner.host_discovery import *
from flask import jsonify


def scan_task():
    pass


def host_discovery_task(host):
    """

    :param host:
    :return:
    """
    try:
        result = list(scan_arp(target=host))
        # запись результата в базу данных
        host_discovery_data = Storage(db='host_discovery', collection='result')
        for host_discovery in result:
            data_ip = host_discovery_data.get_one({"ip": host_discovery})
            if data_ip.count() == 0:
                host_discovery_data.insert({"ip": host_discovery, "tag": None, "time": time()})
                # оповещение (запись в mongo)
                notifications_data = Storage(db='notification', collection='notifications')
                notifications_data.insert({"time": time(), "message": f"New IP: {host_discovery}"})
            else:
                host_discovery_data.upsert({"ip": host_discovery}, {"time": time()})
        return jsonify("success")
    except Exception as e:
        status = "error: {}".format(e)
        return status
