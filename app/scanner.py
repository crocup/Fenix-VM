import nmap


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
        nm_scan.scan(hosts=self.host, ports=self.ports, arguments=self.arguments)
        for host in nm_scan.all_hosts():
            print('Host : %s (%s)' % (host, nm_scan[host].hostname()))
            print('State : %s' % nm_scan[host].state())
            for proto in nm_scan[host].all_protocols():
                print('----------')
                print('Protocol : %s' % proto)
                lport = nm_scan[host][proto].keys()
                for port in lport:
                    print('port : %s\tname : %s\tproduct: %s\tversion : %s' % (
                        port, nm_scan[host][proto][port]['name'],
                        nm_scan[host][proto][port]['product'],
                        nm_scan[host][proto][port]['version']))
