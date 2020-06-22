import nmap
from app import time, db
from app.models import InventoryPost, ScannerPost


class Scanner(object):

    def __init__(self, host, arguments='-sV --host-timeout 10m', ports='1-65535'):
        """

        :param arguments:
        :param ports:
        """
        self.host = host
        self.arguments = arguments
        self.ports = ports

    # # res_id = InventoryPost('192.168.100.1', '2020-01-18')
    # # db.session.add(res_id)
    # # db.session.commit()
    # # res_id = InventoryPost('192.168.100.2', '2020-01-19')
    # # db.session.add(res_id)
    # # db.session.commit()
    # some_owner = InventoryPost.query.filter_by(ip='192.168.100.2').first()
    # print(some_owner)
    # # clifford = ScannerPost(port='53', service_name='dns', service_version='1.9', dateofreg='2020-19-18', owner=some_owner)
    # # db.session.add(clifford)
    # # db.session.commit()
    # some_owner = InventoryPost.query.filter_by(ip='192.168.100.1').first()
    # r = some_owner.scanners
    # print(r)
    # for i in r:
    #     print(i.port)

    def scanner_nmap(self):
        """

        :return:
        """
        nm_scan = nmap.PortScanner()
        nm_scan.scan(hosts=self.host, ports=self.ports, arguments=self.arguments)
        for host in nm_scan.all_hosts():
            print('Host : %s (%s)' % (host, nm_scan[host].hostname()))
            print('State : %s' % nm_scan[host].state())
            for proto in nm_scan[host].all_protocols():
                print('----------')
                print('Protocol : %s' % proto)
                lport = nm_scan[host][proto].keys()
                for port in lport:
                    some_owner = InventoryPost.query.filter_by(ip=host).first()
                    clifford = ScannerPost(protocol=proto, port=port,
                                           service_name=nm_scan[host][proto][port]['product'],
                                           service_version=nm_scan[host][proto][port]['version'],
                                           dateofreg=time(),
                                           owner=some_owner)
                    db.session.add(clifford)
                    print('port : %s\tname : %s\tproduct: %s\tversion : %s' % (
                        port, nm_scan[host][proto][port]['name'],
                        nm_scan[host][proto][port]['product'],
                        nm_scan[host][proto][port]['version']))
        db.session.commit()
        some_owner = InventoryPost.query.filter_by(ip='192.168.100.1').first()
        r = some_owner.scanners
        print(r)
