from app.core.config import API_PREFIX, PROJECT_NAME, DATABASE_IP, DATABASE_PORT, VERSION
from app.core.setting import Settings


def test_data_config_default():
    assert API_PREFIX == "/api/v1"
    assert PROJECT_NAME == "FSEC VM"
    assert VERSION == "0.0.21"
    assert DATABASE_IP == "127.0.0.1"
    assert DATABASE_PORT == 27017


def test_setting():
    assert Settings().app_name == PROJECT_NAME
    assert Settings().app_version == VERSION
    assert Settings().admin_email == "patunutap@gmail.com"
