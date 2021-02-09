"""
Сервис обнаружения хостов в сети
Для работы сервиса используется nmap3
Автор: Dmitry Livanov, 2020
"""
import re
import flask
import nmap3
from flask import jsonify, request, abort

app = flask.Flask(__name__)


@app.route('/api/v1/host_discovery/get', methods=['POST'])
def host_discovery_arp():
    """
    Обнаружение хостов в сети
    :return: массив данных в json
    """
    try:
        if not request.json or not 'host' in request.json:
            abort(400)
        data = request.json
        clients_list = []
        hd_scan = nmap3.NmapHostDiscovery()
        result = hd_scan.nmap_no_portscan(data['host'])
        for res in result:
            check_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", res)
            if check_ip:
                ip = check_ip.group()
                clients_list.append(ip)
    except Exception as e:
        print(e)
        clients_list = []
    return jsonify({"data": clients_list})


if __name__ == '__main__':
    app.run(port=9001)
