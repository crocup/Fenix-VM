import datetime

import pymongo

from app import db, time
from app.models import InventoryPost, ScannerPost, ResultPost


def Scanner_Data_Record(host, proto, port, product, version, uuid, state, name):
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
    scanford = ScannerPost(protocol=proto, port=port, service_name=product, service_version=version,
                           dateofreg=time(), owner=some_owner, ip=host, uuid=uuid, state=state, name=name)
    db.session.add(scanford)
    db.session.commit()


def Scanner_Data_Filter_UUID(uid):
    dictionary = {}
    service_list = []
    r = ScannerPost.query.filter(ScannerPost.uuid == str(uid))
    for i in r:
        tag_ip = Inventory_Data_Filter_IP(i.ip)
        dictionary = {
            'ip': i.ip,
            'dateofreg': i.dateofreg,
            'uuid': uid,
            'tag': tag_ip['tag'],
            'port': []
        }
        s_ver = {
            'port': i.port,
            'protocol': i.protocol,
            'name': i.name,
            'service_name': i.service_name,
            'service_version': i.service_version,
            'state': i.state
        }
        service_list.append(s_ver)
        for item in service_list:
            dictionary['port'].append(item)
    return dictionary


def Scanner_Data_All():
    result = db.session.query(ScannerPost.ip, ScannerPost.dateofreg, ScannerPost.uuid).group_by(ScannerPost.uuid).all()
    return result


def Inventory_Data_All():
    return InventoryPost.query.all()


def Inventory_Data_Record(result_inventory):
    """

    :param result_inventory:
    :return:
    """
    for res in result_inventory:
        ips_find = InventoryPost.query.filter_by(ip=res).first()
        if ips_find is None:
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


def Result_Data(uid, name, time):
    res_id = ResultPost(uid, name, time)
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
    mng = pymongo.MongoClient()
    dbs = mng['scanner']
    posts = dbs['vulnerability']
    sets = {
        "id": str(task),
        "result": data,
        "name": name,
        "port": port,
        "port_name": port_name,
        "last_update": now.strftime("%d-%m-%Y %H:%M")
    }
    posts.insert(sets)
    mng.close()
