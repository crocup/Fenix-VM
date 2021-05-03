import asyncio
import requests

from app import basedir


class FenixWebBuster:

    def __init__(self, url):
        """

        :param url:
        """
        self.dict = basedir+"/plugins/dir_buster/data/common.txt"
        self.data = []
        self.url = url

    async def fastdirb(self, path):
        """

        :param path:
        :return:
        """
        path = path.strip().decode("utf-8")
        urlpath = self.url + "/" + path
        r = requests.get(urlpath)
        if r.status_code == 200:
            self.data.append({
                "code": r.status_code,
                "url": urlpath
            })

    async def run(self):
        """

        :return:
        """
        wordlist = open(self.dict, "rb")
        try:
            await asyncio.wait([
                self.fastdirb(path)
                for path in wordlist.readlines()
            ])
        except:
            self.data = []
        return self.data


def TaskWebBuster(url):
    task = FenixWebBuster(url=url)
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(task.run())
    loop.close()
    return results
