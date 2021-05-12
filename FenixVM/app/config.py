import os

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = False
HOST_DISCOVERY = "http://127.0.0.1:9001/api/v1/discovery"
API_VULNDB = 'api'
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
