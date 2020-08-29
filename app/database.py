from app import db, time
from app.models import InventoryPost, ScannerPost


def record_scan(host, proto, port, product, version, uuid):
    """

    :param host:
    :param proto:
    :param port:
    :param product:
    :param version:
    :return:
    """
    some_owner = InventoryPost.query.filter_by(ip=host).first()
    scanford = ScannerPost(protocol=proto, port=port, service_name=product, service_version=version,
                           dateofreg=time(), owner=some_owner, ip=host, uuid=uuid)
    db.session.add(scanford)
    db.session.commit()


def group_by_inventory(ip):
    dictionary = {}
    r = InventoryPost.query.filter(InventoryPost.ip == str(ip))
    for i in r:
        dictionary = {
            'ip': i.ip,
            'tag': i.tags,
            'dateofreg': i.dateofreg,
        }
    return dictionary


def group_ip_date():
    return db.session.query(ScannerPost.ip, ScannerPost.dateofreg, ScannerPost.uuid).group_by(ScannerPost.uuid).all()


def group_by(uid):
    dictionary = {}
    service_list = []
    r = ScannerPost.query.filter(ScannerPost.uuid == str(uid))

    for i in r:
        dictionary = {
            'ip': i.ip,
            'dateofreg': i.dateofreg,
            'uuid': uid,
            'port': []
        }
        s_ver = {
            'port': i.port,
            'protocol': i.protocol,
            'service_name': i.service_name,
            'service_version': i.service_version
        }
        service_list.append(s_ver)
        for item in service_list:
            dictionary['port'].append(item)

    return dictionary
