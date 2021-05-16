"""
Dmitry Livanov, 2021
"""
from abc import abstractmethod
from typing import Dict


class AbstractCount:
    """
    Абстрактный класс для подсчета данных в dict
    """

    def template_count(self, data: Dict) -> int:
        """
        Функция-шаблон
        return: Count
        """
        return self.count_data(data)

    @abstractmethod
    def count_data(self, data: Dict) -> int:
        pass


class VulnCountData(AbstractCount):

    def count_data(self, data: Dict) -> int:
        count = 0
        for info_port in data['open_port']:
            count += len(info_port['plugins']['cve_mitre'])
        return count


class ExploitCountData(AbstractCount):

    def count_data(self, data: Dict) -> int:
        count = 0
        return count


class DirCountData(AbstractCount):

    def count_data(self, data: Dict) -> int:
        count = 0
        return count


class PassCountData(AbstractCount):

    def count_data(self, data: Dict) -> int:
        count = 0
        return count


def result_count(abstract_class: AbstractCount, data: Dict) -> int:
    return abstract_class.template_count(data)
