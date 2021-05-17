# -*- coding: utf-8 -*-

class BasePlugin(object):
    def run(self, **kwargs):
        """
        Базовая функция по созданию плагинов
        def run(self, **kwargs):
        if kwargs is not None:
            if (('product' in kwargs) and (kwargs['product'] is not None)) and \
                    (('version' in kwargs) and (kwargs['version'] is not None)):
                result_cvemitre = result_code(CveMitre(), product=kwargs['product'], version=kwargs['version'])
                return {'cve_mitre': result_cvemitre['data']}
        :param kwargs: принимает параметры proto, product, version, url, port
        :return:
        """
        pass
