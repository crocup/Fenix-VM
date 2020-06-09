import nmap
from pprint import pprint


class Scanner(object):

    def __init__(self, host, arguments='-sV --host-timeout 10m', ports='1-65535'):
        """

        :param arguments:
        :param ports:
        """
        self.host = host
        self.arguments = arguments
        self.ports = ports

    def scanner_nmap(self):
        """

        :return:
        """
        nm_scan = nmap.PortScanner()
        res = nm_scan.scan(hosts=self.host, ports=self.ports, arguments=self.arguments)
        pprint(res)
