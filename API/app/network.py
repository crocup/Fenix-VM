import ipaddress
import logging


def check_ip(host):
    """Проверка ip или маски сети"""
    try:
        if format(ipaddress.IPv4Network(host)):
            return True
        if format(ipaddress.IPv4Address(host)):
            return True
        return False
    except Exception as e:
        logging.error(e)
        return False