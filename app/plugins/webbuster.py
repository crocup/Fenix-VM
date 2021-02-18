# Описание
# Dmitry Livanov, 2021
import subprocess
import re
from typing import Dict

version = '0.0.1 (default, Feb 16 2021)'
platform = 'linux'


def DirectoryBuster(service: str, host: str, port: int) -> Dict:
    """

    :param service:
    :param host:
    :param port:
    :return: Dict
    """
    if (service == 'http' and port == 80) or (service == 'https' and port == 443):
        url = f"{service}://{host}"
    else:
        url = f"{service}://{host}:{port}"
    list_dir = []
    process = subprocess.Popen([r'dirb', url, '-f'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in iter(process.stdout.readline, b''):
        line_dir = line.rstrip()
        result = re.search(br'CODE', line_dir)
        if result is not None:
            list_dir.append(str(line_dir).decode('UTF-8'))
    data = {
        "data": list_dir
    }
    return data
