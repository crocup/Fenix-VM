"""
info.html
Dmitry Livanov, 2021
"""
from __future__ import annotations
from abc import abstractmethod
from pprint import pprint
from app.config import MONGO_PORT, MONGO_HOST
from app.service.database import MessageProducer, MongoDriver


class AbstractStatistic:
    """
    Абстрактный класс для работы с информацией по конретной задаче
    """

    def __init__(self, uuid):
        """
        uuid: uuid конкретной задачи
        """
        self.uuid = uuid

    def template_count_data(self):
        """
        шаблонный метод для подсчета данных
        """
        return self.count_data(self.get_uuid())

    def template_info_data(self):
        """
        шаблонный метод для вывода информации о задаче
        """
        return self.info_data(self.get_uuid())

    def get_uuid(self) -> None:
        """
        return: результат из базы данных
        """
        scanner_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                   base="scanner", collection="result"))
        return scanner_data.get_message(message={"uuid": self.uuid})

    @abstractmethod
    def count_data(self, data):
        """

        """
        pass

    @abstractmethod
    def info_data(self, data):
        """

        """
        pass


class DirectoryInfo(AbstractStatistic):

    def count_data(self, data):
        count = 0
        for i in data:
            if 'open_port' in i:
                for info_directory in i['open_port']:
                    if 'directory' in info_directory:
                        count += len(info_directory['directory'])
        data = {
            "count": count,
        }
        return data

    def info_data(self, data):
        pass


def result_count_data(abstract_class: AbstractStatistic):
    return abstract_class.template_count_data()


def delete_task(uuid: str):
    """
    Удаление информации о задаче
    uuid: UUID номер задачи
    """
    try:
        message_mongo = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                    base="scanner", collection="result"))
        message_mongo.delete_message({"uuid": uuid})
    except Exception as e:
        print(e)


def vulnerability_info(vulnerability: str):
    """
    получение информации о CVE
    """
    try:
        cve_upper = str(vulnerability).upper()
        message_mongo = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                    base="vulndb", collection="cve"))
        data = message_mongo.get_message({"cve": cve_upper})
        return data
    except Exception as e:
        print(e)