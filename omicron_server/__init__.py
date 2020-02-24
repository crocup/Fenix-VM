import logging.config
from flask import Flask, request, jsonify
from rq import Queue
from redis import Redis
import configparser
from .components.inventory import *
from .components.scanner import *
from .components.record_database import *
from .components.full_scan import *
from .components.search_vulnerability import *
from omicron_server import scheduler

app = Flask(__name__)
q = Queue(connection=Redis(), default_timeout=3600)

# create the logging file handler
logging.config.fileConfig('setting/log.conf')
logger = logging.getLogger("OmicronApp")

# read settings file
_path = "setting/settings.conf"
config = configparser.ConfigParser()
config.read(_path)
logger.info("Server start...")

vulnerabilities_api = VulnerabilitySearch(
            vulners_api=config.get("VULNERS", "API"))
from . import views
