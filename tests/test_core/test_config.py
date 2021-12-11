from app.core.config import *
from app.core.setting import Settings


def test_data_config_default():
    assert API_PREFIX == "/api/v1"
    assert PROJECT_NAME == "FSEC VM"
    assert VERSION == "0.0.21"
    assert DATABASE_IP == "0.0.0.0"
    assert DATABASE_PORT == 27017
    assert BASE_VM == "VM"
    assert COLLECTION_HOST_DISCOVERY == "discovery"
    assert COLLECTION_SCANNER == "scanner"


def test_setting():
    assert Settings().APP_NAME == PROJECT_NAME
    assert Settings().APP_VERSION == VERSION
    assert Settings().ADMIN_MAIL == "patunutap@gmail.com"
    assert Settings().MASK == "192.168.1.0/24"

