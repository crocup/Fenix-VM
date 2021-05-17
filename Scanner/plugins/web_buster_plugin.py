import os
import requests
from base_plugin import BasePlugin


def task_dir_buster(url):
    try:
        data = []
        wordlist = open(os.path.abspath(os.path.dirname(__file__)) + "/data/common.txt", "rb")
        for path in wordlist.readlines():
            path = path.strip().decode("utf-8")
            urlpath = url + "/" + path
            r = requests.get(urlpath, timeout=10)
            if r.status_code == 200:
                data.append({
                    "code": r.status_code,
                    "url": urlpath
                })
    except Exception as e:
        data = []
    return data


class FenixWebBuster(BasePlugin):
    """

    """

    def __init__(self):
        """

        :param url:
        """

    def run(self, **kwargs):
        if kwargs is not None:
            if 'proto' and 'url' in kwargs:
                if kwargs['proto'] is not None and kwargs['url'] is not None:
                    if kwargs['proto'] == 'http':
                        """
                        Сюда пишем код
                        """
                        return {'directory': kwargs['proto']}
