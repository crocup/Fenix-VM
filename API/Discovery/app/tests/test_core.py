import pytest
from app.core.config import *
from app.service.network import check_ip


def test_check_ip():
    assert check_ip("192.168.100.0/24") == True
    assert check_ip("192.168.100.1") == True
    assert check_ip("300.168.100.1") == False
    assert check_ip("300.168.100.0/8") == False
    assert check_ip("test/8") == False


def test_check_setting():
    assert settings.CORE_IP == "localhost"
    assert settings.DEBUG == True
