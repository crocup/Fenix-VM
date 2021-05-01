import re
from datetime import datetime
from typing import List, Dict
import nmap3
from database import MessageProducer, MongoDriver


def get_time() -> str:
    """

    """
    now = datetime.now()
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time


def get_hosts(host: str) -> Dict[str, List[str]]:
    """

    """
    clients_list = []
    try:
        hd_scan = nmap3.NmapHostDiscovery()
        result = hd_scan.nmap_no_portscan(host)
        for res in result:
            check_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res)
            if check_ip:
                ip = check_ip.group()
                clients_list.append(ip)
    except Exception as e:
        clients_list = []
    record_result(data=clients_list)
    return {"result": clients_list}


def record_result(data: List):
    """

    """
    try:
        for host_discovery in data:
            message_host_discovery = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                                 base='host_discovery', collection='result'))
            message_notification = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                               base='notification', collection='notifications'))
            data_ip = message_host_discovery.get_message({"ip": str(host_discovery)})
            if data_ip is None:
                message_host_discovery.insert_message({"ip": host_discovery, "tag": "None", "time": get_time()})
                message_notification.insert_message({"time": get_time(), "message": f"New IP: {host_discovery}"})
            else:
                message_host_discovery.update_message(message={"ip": host_discovery}, new_value={"time": get_time()})
    except Exception as e:
        print(e)