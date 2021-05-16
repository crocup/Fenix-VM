import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'tes873465'
    MONGO_HOST = "127.0.0.1"
    MONGO_PORT = 27017
    API_VULNDB = ""
    HOST_DISCOVERY="http://127.0.0.1:9001/api/v1/discovery"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
