import requests
from app import basedir


class FenixWebBuster:
    """

    """

    def __init__(self, url):
        """

        :param url:
        """
        self.dict = basedir+"/plugins/dir_buster/data/common.txt"
        self.data = []
        self.url = url

    def task_dir_buster(self):
        try:
            wordlist = open(self.dict, "rb")
            for path in wordlist.readlines():
                path = path.strip().decode("utf-8")
                urlpath = self.url + "/" + path
                r = requests.get(urlpath, timeout=10)
                if r.status_code == 200:
                    self.data.append({
                        "code": r.status_code,
                        "url": urlpath
                    })
                    print({
                        "code": r.status_code,
                        "url": urlpath
                    })
        except Exception as e:
            self.data = []
        return self.data
