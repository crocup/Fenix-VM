from abc import abstractmethod
import datetime
from uuid import uuid4
from nmap3 import nmap3
from app.config import MONGO_HOST, MONGO_PORT
from app.plugins.dir_buster.fenix_web_buster import FenixWebBuster
from app.plugins.vulnerability import result_code, CveMitre
from app.service.database import MessageProducer, MongoDriver


class Scanner:
    def __init__(self, host):
        """

        :param host:
        """
        self.host = host

    def scan_service_version(self):
        """

        :return:
        """
        nm = nmap3.Nmap()
        return nm.nmap_version_detection(self.host)

    def scan_arp(self):
        """

        :return:
        """
        arp_nmap = nmap3.NmapHostDiscovery()
        return arp_nmap.nmap_arp_discovery(self.host)

    def scan_ping(self):
        """

        :return:
        """
        nm_ping = nmap3.NmapScanTechniques()
        return nm_ping.nmap_ping_scan(self.host)

    def scan_subnet(self):
        """

        :return:
        """
        nm = nmap3.Nmap()
        return nm.nmap_subnet_scan(self.host)


class AbstractScanner:

    def __init__(self, host):
        """
        uuid: uuid конкретной задачи
        """
        self.host = host
        self.result = dict()
        self.uuid = self.get_uuid()

    def template_scanner(self):
        # scan
        self.scanner()
        # count
        self.count_vulnerability()
        self.count_exploit()
        self.count_directory()
        self.count_pass()
        # info
        self.info_scanner()
        # avg score
        self.score()
        # record in mongo
        self.record_data()

    def get_uuid(self):
        uuid = str(uuid4())
        self.result['host'] = self.host
        self.result['uuid'] = uuid
        now = datetime.datetime.now()
        self.result['date'] = now.strftime("%d-%m-%Y %H:%M")
        host_discovery_tag = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                         base="HostDiscovery", collection="result"))
        tag_ip = host_discovery_tag.get_message(message={"ip": self.host})
        for tags in tag_ip:
            self.result['tag'] = tags['tag']
        scanner_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                   base="scanner", collection="result"))
        scanner_data.insert_message(message=self.result)
        return uuid

    @abstractmethod
    def scanner(self):
        pass

    @abstractmethod
    def score(self):
        pass

    @abstractmethod
    def count_vulnerability(self):
        pass

    @abstractmethod
    def count_exploit(self):
        pass

    @abstractmethod
    def count_directory(self):
        pass

    @abstractmethod
    def count_pass(self):
        pass

    @abstractmethod
    def info_scanner(self):
        pass

    @abstractmethod
    def record_data(self):
        pass


class ScannerTask(AbstractScanner):

    def scanner(self):
        open_ports = []
        task = Scanner(self.host)
        result = task.scan_service_version()
        scann_port = result[self.host]['ports']
        for i in scann_port:
            prt = dict()
            prt['port'] = i['portid']
            prt['protocol'] = i['protocol']
            prt['state'] = i['state']
            prt['name'] = None
            prt['product'] = None
            prt['version'] = None
            if 'cpe' in i:
                for cpe_data in i['cpe']:
                    prt['cpe'] = cpe_data['cpe']
            prt['plugins'] = {'cve_mitre': []}
            if 'service' in i:
                if 'name' in i['service']:
                    prt['name'] = i['service']['name']
                    if 'product' in i['service']:
                        prt['product'] = i['service']['product']
                        if 'version' in i['service']:
                            prt['version'] = i['service']['version']
            # FenixWebBuster
            if prt['name'] == 'http':
                url = f"http://{self.host}:{prt['port']}"
                dirb = FenixWebBuster(url)
                prt['directory'] = dirb.task_dir_buster()
            # cve mitre
            if prt['product'] is not None and prt['version'] is not None:
                result_cvemitre = result_code(CveMitre(), product=prt['product'], version=prt['version'])
                prt['plugins'] = {'cve_mitre': result_cvemitre['data']}
            open_ports.append(prt)
        self.result['open_port'] = open_ports

    def score(self):
        if self.result['count_data'] == 0:
            self.result['score'] = 0
        else:
            self.result['score'] = 9.99

    def count_vulnerability(self):
        count = 0
        for info_port in self.result['open_port']:
            count += len(info_port['plugins']['cve_mitre'])
        self.result['count_data'] = count

    def count_exploit(self):
        self.result['count_exploit'] = 0

    def count_directory(self):
        self.result['count_directory'] = 0

    def count_pass(self):
        self.result['count_pass'] = 0

    def info_scanner(self):
        self.result['info_scanner'] = {}

    def record_data(self):
        message_mongo = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                    base="scanner", collection="result"))
        message_mongo.update_message(message={"uuid": self.uuid}, new_value=self.result)


def result_scanner(abstract_class: AbstractScanner):
    return abstract_class.template_scanner()
