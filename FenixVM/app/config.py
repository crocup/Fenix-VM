import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
HOST_DISCOVERY = "http://127.0.0.1:9001/api/v1/discovery"
SCANNER = "http://127.0.0.1:9101/api/v1/scanner"
API_VULNDB = os.environ.get('API_VULNDB')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
