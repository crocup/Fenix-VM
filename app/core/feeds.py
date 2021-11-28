from abc import abstractmethod


class AbstractDownloadFeeds:
    """

    """

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def template_download_vulnerability(self):
        self.download_feeds()
        self.send_db()

    @abstractmethod
    def send_db(self):
        pass

    @abstractmethod
    def download_feeds(self):
        pass


def result_download_vulnerability(abstract_class: AbstractDownloadFeeds):
    abstract_class.template_download_vulnerability()
