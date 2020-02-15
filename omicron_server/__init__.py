import logging.config
import time
from flask import Flask, request, jsonify
from rq import Queue
from redis import Redis
import configparser
import schedule
from .components.inventory import *
from .components.scanner import *
from .components.record_database import *
from .components.full_scan import *
from .components.search_vulnerability import *
from .components.scheduler import *

app = Flask(__name__)
q = Queue(connection=Redis(), default_timeout=3600)
log_path = "omicron_server/logs/"
if not os.path.exists(log_path):
    os.mkdir(log_path)
setting_path = "omicron_server/settings/"
if not os.path.exists(setting_path):
    os.mkdir(setting_path)

# create the logging file handler
logging.config.fileConfig("omicron_server/settings/log.conf")
log = logging.getLogger("SpotterApp")

# read settings file
_path = "omicron_server/settings/settings.conf"
config = configparser.ConfigParser()
config.read(_path)

from . import views

# run scheduler
target_ips = config.get("NETWORK_IP", "IP")
# time in hours
sched_inventory = config.get("SCHEDULER", "INVENTORY")
sched_full_scanner = config.get("SCHEDULER", "FULL_SCAN")
sched = SchedulerScanner(target_mask=target_ips)
schedule.every(int(sched_inventory)).hour.do(sched.inventory_scheduler())
schedule.every(int(sched_full_scanner)).hour.do(sched.full_scan_scheduler())
while True:
    schedule.run_pending()
    time.sleep(1)
