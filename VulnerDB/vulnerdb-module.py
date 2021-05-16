import logging.config
import os
import time
from components.record_database import RecordMongo
import wget
import zipfile
import configparser
import schedule
from dotenv import load_dotenv

json_path = "json/"
if not os.path.exists(json_path):
    os.mkdir(json_path, 0o755)
log_path = "logs/"
if not os.path.exists(log_path):
    os.mkdir(log_path, 0o755)
setting_path = "setting/"
if not os.path.exists(setting_path):
    os.mkdir(setting_path, 0o755)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# read setting file
path = "setting/settings_vulner.conf"
config = configparser.ConfigParser()
config.read(path)

# create the logging file handler
logging.config.fileConfig('setting/log_vulner.conf')
log = logging.getLogger("VulnerDB")


def download(years):
    """
    download feeds cve
    :param years: finish year feeds
    :return: None
    """
    try:
        record_in_mongo = RecordMongo(db=config.get("DATABASE_VULNERDB", "BASE"),
                                      coll=config.get("DATABASE_VULNERDB", "COLLECTION"))
        for year in range(2002, int(years)):
            log.info(year)
            name = 'nvdcve-1.1-'+str(year)+'.json.zip'
            name_json = 'nvdcve-1.1-'+str(year)+'.json'
            url = 'https://nvd.nist.gov/feeds/json/cve/1.1/'+str(name)
            wget.download(url, 'json/'+str(name))
            unzip(name)
            os.remove('json/'+str(name))
            record_in_mongo.database_vulner(name_json=name_json)
            os.remove('json/' + str(name_json))
        record_in_mongo.close_connection()
    except Exception as error:
        log.error(error)


def unzip(name):
    """
    unzip feeds
    :param name: name zip file
    :return: None
    """
    try:
        cve_zip = zipfile.ZipFile('json/'+str(name))
        cve_zip.extractall('json/')
        cve_zip.close()
    except Exception as error:
        log.error(error)


def run():
    try:
        last_year = config.get("CONFIG", "YEAR")
        log.info("Program start")
        schedule.every().day.at(str(config.get("CONFIG", "TIME_SCAN"))).do(download(years=last_year))
        log.info("Program sleep")
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as error:
        log.error(error)


if __name__ == "__main__":
    run()
