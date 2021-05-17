from abc import abstractmethod
import datetime
from uuid import uuid4
from nmap3 import nmap3
import conf
from database import MessageProducer, MongoDriver
import data_count
import os
import inspect
from plugins.base_plugin import BasePlugin

plugin_dir = "plugins"

# Сюда добавляем имена загруженных модулей
modules = []

# Перебирем файлы в папке plugins
for fname in os.listdir(plugin_dir):
    # Нас интересуют только файлы с расширением .py
    if fname.endswith(".py"):
        # Обрежем расширение .py у имени файла
        module_name = fname[: -3]

        # Пропустим файлы base.py и __init__.py
        if module_name != "base_plugin" and module_name != "__init__":
            # Загружаем модуль и добавляем его имя в список загруженных модулей
            package_obj = __import__(plugin_dir + "." + module_name)
            modules.append(module_name)


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
        return nm.nmap_version_detection(self.host, args="-sV -T4 --host-timeout 10m")

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
        self.scanner()
        self.mcount()
        self.info()
        self.score()
        self.record_data()

    def get_uuid(self):
        uuid = str(uuid4())
        self.result['host'] = self.host
        self.result['uuid'] = uuid
        now = datetime.datetime.now()
        self.result['date'] = now.strftime("%d-%m-%Y %H:%M")
        host_discovery_tag = MessageProducer(MongoDriver(host=conf.Config.MONGO_HOST, port=conf.Config.MONGO_PORT,
                                                         base="HostDiscovery", collection="result"))
        tag_ip = host_discovery_tag.get_message(message={"ip": self.host})
        self.result['tag'] = tag_ip['tag']
        scanner_data = MessageProducer(MongoDriver(host=conf.Config.MONGO_HOST, port=conf.Config.MONGO_PORT,
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
    def mcount(self):
        pass

    @abstractmethod
    def info(self):
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
            # Перебираем загруженные модули
            for modules_name in modules:
                module_obj = getattr(package_obj, modules_name)
                for elem in dir(module_obj):
                    obj = getattr(module_obj, elem)
                    if inspect.isclass(obj):
                        if issubclass(obj, BasePlugin):
                            a = obj()
                            res_pl = a.run(proto=prt['name'], url=f"http://{self.host}:{prt['port']}", port=prt['port'],
                                           product=prt['product'], version=prt['version'], host=self.host)
                            if res_pl is not None:
                                prt['plugins'] = res_pl
            # Добавление портов в dict
            open_ports.append(prt)
        self.result['open_port'] = open_ports

    def score(self):
        if self.result['count_data'] == 0:
            self.result['score'] = 0
        else:
            self.result['score'] = 9.99

    def mcount(self):
        self.result['count_data'] = data_count.result_count(data_count.VulnCountData(), self.result)
        self.result['count_exploit'] = data_count.result_count(data_count.ExploitCountData(), self.result)
        self.result['count_directory'] = data_count.result_count(data_count.DirCountData(), self.result)
        self.result['count_pass'] = data_count.result_count(data_count.PassCountData(), self.result)

    def info(self):
        self.result['info_scanner'] = {}

    def record_data(self):
        message_mongo = MessageProducer(MongoDriver(host=conf.Config.MONGO_HOST, port=conf.Config.MONGO_PORT,
                                                    base="scanner", collection="result"))
        message_mongo.update_message(message={"uuid": self.uuid}, new_value=self.result)


def result_scanner(abstract_class: AbstractScanner):
    return abstract_class.template_scanner()
