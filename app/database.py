import datetime
import json
from pprint import pprint

from app import db, time, db_scanner, db_vulnerability, db_notification
from app.models import InventoryPost, ScannerPost, ResultPost


def Scanner_Data_Record(host, uuid):
    """

    :param name:
    :param state:
    :param uuid:
    :param host:
    :param proto:
    :param port:
    :param product:
    :param version:
    :return:
    """
    some_owner = InventoryPost.query.filter_by(ip=host).first()
    scanford = ScannerPost(dateofreg=time(), owner=some_owner, ip=host, uuid=uuid)
    db.session.add(scanford)
    db.session.commit()


def Scanner_Data_Filter_UUID(uid):
    return db_vulnerability.result.find({"uuid": uid})


def Scanner_Data_All():
    result = db.session.query(ScannerPost.ip, ScannerPost.dateofreg, ScannerPost.uuid).group_by(ScannerPost.uuid).all()
    return result


def Inventory_Data_All():
    inventory_all = []
    for i in InventoryPost.query.all():
        # print(j, i)
        ip_res = {
            'ip': i.ip,
            'uuid': i.uid,
            'tag': i.tags,
            'date': i.dateofreg
        }
        inventory_all.append(ip_res)
    inventory_json = json.dumps(inventory_all, indent=4)
    data = json.loads(inventory_json)
    return data


def Inventory_Data_Record(result_inventory):
    """

    :param result_inventory:
    :return:
    """
    for res in result_inventory:
        ips_find = InventoryPost.query.filter_by(ip=res).first()
        if ips_find is None:
            # если появился новый ip
            result_json = {
                "time": time(),
                "message": f"New IP: {res}"
            }
            posts = db_notification["notifications"]
            posts.insert(result_json)
            reg = InventoryPost(res, time())
            db.session.add(reg)
        else:
            ips_find.dateofreg = time()
            db.session.add(ips_find)
    db.session.commit()


def Inventory_Tag_Record(ip, tag):
    ips_find = InventoryPost.query.filter_by(ip=ip).first()
    ips_find.tags = tag
    db.session.add(ips_find)
    db.session.commit()


def Inventory_Data_Filter_IP(ip):
    dictionary = {}
    r = InventoryPost.query.filter(InventoryPost.ip == str(ip))
    for i in r:
        dictionary = {
            'ip': i.ip,
            'tag': i.tags,
            'dateofreg': i.dateofreg,
        }
    return dictionary


def Inventory_Data_Delete(ip):
    """

    :param ip:
    :return:
    """
    InventoryPost.query.filter_by(ip=ip).delete()
    db.session.commit()


def Result_Data(uid, name, host, time):
    res_id = ResultPost(uid, name, host, time)
    db.session.add(res_id)
    db.session.commit()


def Vulnerability_Data_Record(data, name, task, port, port_name):
    """

    :param task:
    :param name:
    :param data:
    :return:
    """
    now = datetime.datetime.now()
    posts = db_vulnerability['vulnerability']
    sets = {
        "id": str(task),
        "result": data,
        "name": name,
        "port": port,
        "port_name": port_name,
        "last_update": now.strftime("%d-%m-%Y %H:%M")
    }
    posts.insert(sets)


def ssh_bruteforce_data_record(task, data, name, port):
    now = datetime.datetime.now()
    posts = db_scanner['ssh']
    sets = {
        "id": str(task),
        "result": data,
        "name": name,
        "port": port,
        "last_update": now.strftime("%d-%m-%Y %H:%M")
    }
    posts.insert(sets)


def web_bruteforce_data_record(task, data, name, port):
    now = datetime.datetime.now()
    posts = db_scanner['web']
    sets = {
        "id": str(task),
        "result": data,
        "name": name,
        "port": port,
        "last_update": now.strftime("%d-%m-%Y %H:%M")
    }
    posts.insert(sets)
