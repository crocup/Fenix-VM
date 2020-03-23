import os
import wget
import omicron_server
import schedule
from time import sleep
import zipfile


def run():
    """

    :return:
    """
    try:
        target_ips = omicron_server.config.get("NETWORK_IP", "IP")
        sched_inventory = omicron_server.config.get("SCHEDULER", "INVENTORY")
        sched_full_scanner = omicron_server.config.get("SCHEDULER", "FULL_SCAN")
        sched_cve_database = omicron_server.config.get("SCHEDULER", "CVE")
        years_cve = omicron_server.config.get("CONFIG_CVE", "YEAR")
        sched = SchedulerScanner(target_mask=target_ips)
        schedule.every(int(sched_inventory)).hours.do(sched.inventory_scheduler)
        schedule.every(int(sched_full_scanner)).hours.do(sched.full_scan_scheduler)
        schedule.every(int(sched_cve_database)).hours.do(download_cve(years=years_cve))
        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        omicron_server.logger.error(e)


def unzip_cve(name):
    """
    unzip feeds
    :param name: name zip file
    :return: None
    """
    try:
        cve_zip = zipfile.ZipFile('json/' + str(name))
        cve_zip.extractall('json/')
        cve_zip.close()
    except Exception as error:
        omicron_server.logger.error(error)


def download_cve(years):
    """
    download feeds cve
    :param years: finish year feeds
    :return: None
    """
    try:
        record_in_mongo = omicron_server.RecordMongo(db=omicron_server.config.get("DATABASE_CVE", "BASE"),
                                                     coll=omicron_server.config.get("DATABASE_CVE", "COLLECTION"))
        for year in range(2002, int(years)):
            name = 'nvdcve-1.1-' + str(year) + '.json.zip'
            name_json = 'nvdcve-1.1-' + str(year) + '.json'
            url = 'https://nvd.nist.gov/feeds/json/cve/1.1/' + str(name)
            wget.download(url, 'json/' + str(name))
            unzip_cve(name)
            os.remove('json/' + str(name))
            record_in_mongo.database_vulner(name_json=name_json)
            os.remove('json/' + str(name_json))
        record_in_mongo.close_connection()
    except Exception as error:
        omicron_server.logger.error(error)


class SchedulerScanner(object):

    def __init__(self, target_mask):
        self.target_mask = target_mask

    def inventory_scheduler(self):
        """

        :return:
        """
        omicron_server.logger.info("start scheduler inventory")
        inventory_service = omicron_server.Inventory(target=self.target_mask)
        inventory_service.result_scan()

    def full_scan_scheduler(self):
        """

        :return:
        """
        omicron_server.logger.info("start scheduler full scanner")
        omicron_server.full_scan(target=self.target_mask)
