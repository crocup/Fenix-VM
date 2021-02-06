import datetime
import json
from app import db, time, db_scanner
# from app.models import InventoryPost, ScannerPost, ResultPost


# def Scanner_Data_Record(host, uuid):
#     """
#
#     :param uuid:
#     :param host:
#     :return:
#     """
#     some_owner = InventoryPost.query.filter_by(ip=host).first()
#     scanford = ScannerPost(dateofreg=time(), owner=some_owner, ip=host, uuid=uuid)
#     db.session.add(scanford)
#     db.session.commit()


# def Inventory_Data_All():
#     inventory_all = []
#     for i in InventoryPost.query.all():
#         ip_res = {
#             'ip': i.ip,
#             'uuid': i.uid,
#             'tag': i.tags,
#             'date': i.dateofreg
#         }
#         inventory_all.append(ip_res)
#     inventory_json = json.dumps(inventory_all, indent=4)
#     data = json.loads(inventory_json)
#     return data


# def Inventory_Data_Delete(host):
#     """
#     Удаление ip адреса из базы данных sqlite
#     :param host:
#     :return:
#     """
#     try:
#         InventoryPost.query.filter_by(ip=host).delete()
#         db.session.commit()
#         print(f"{host} удален")
#     except Exception as e:
#         print(e)


# def Result_Data(uid, name, host, time):
#     res_id = ResultPost(uid, name, host, time)
#     db.session.add(res_id)
#     db.session.commit()


def Vulnerability_Data_Record(data, name, task, port, port_name):
    """

    :param task:
    :param name:
    :param data:
    :return:
    """
    now = datetime.datetime.now()
    posts = db_scanner['vulnerability']
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
