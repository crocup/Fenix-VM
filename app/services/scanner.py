from abc import abstractmethod
from typing import Dict
from nmap3 import nmap3


class AbstractScanner:
    """
    """

    def __init__(self, host):
        self.host = host
        self.nmap = nmap3.Nmap()

    def template_scanner(self):
        result = self.scanner(self.host)
        print(result)

    @abstractmethod
    def scanner(self, host):
        pass


class ServiceDetection(AbstractScanner):
    """ """

    def scanner(self, host) -> Dict:
        """
        """
        return self.nmap.nmap_version_detection(host)


def result_discovery(abstract_class: AbstractScanner):
    """
    """
    abstract_class.template_scanner()
