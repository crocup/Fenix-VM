from abc import abstractmethod
from nmap3 import nmap3


class AbstractScanner:
    def __init__(self, host):
        self.host = host
        self.nmap = nmap3.Nmap()

    def template_scanner(self):
        return self.scanner(self.host)

    @abstractmethod
    def scanner(self, host):
        pass


class FenixScanner(AbstractScanner):
    def scanner(self, host):
        return self.nmap.nmap_version_detection(self.host, args="-sV -T4 --host-timeout 15m")


def result_scanner(abstract_class: AbstractScanner):
    return abstract_class.template_scanner()


class DistributionDB:
    def template(self):
        pass
