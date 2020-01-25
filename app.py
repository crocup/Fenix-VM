import json
import os
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from components.inventory import Inventory
from components.scanner import Scanner

app = Flask(__name__)
q = Queue(connection=Redis(), default_timeout=3600)

log_path = "logs/"
if not os.path.exists(log_path):
    os.mkdir(log_path)
setting_path = "settings/"
if not os.path.exists(setting_path):
    os.mkdir(setting_path)


@app.route('/process/inventory/start', methods=["POST"])
def process_inventory():
    try:
        body_json = request.get_json()
        target_mask = body_json['target']
        inventory_service = Inventory(target=target_mask)
        results = q.enqueue_call(inventory_service.result_scan, result_ttl=500)
        return results.id
    except Exception as e:
        print(e)
        exit(1)


@app.route('/process/scanner/ip/start', methods=["POST"])
def process_scanner_ip():
    try:
        body_json = request.get_json()
        target_ip = body_json['target']
        scanner_service = Scanner(host=target_ip)
        results = q.enqueue_call(scanner_service.scanner_async, result_ttl=500)
        return results.id
    except Exception as e:
        print(e)
        exit(1)


@app.route('/process/scanner/full/start', methods=["POST"])
def process_scanner_full():
    try:
        pass
        # body_json = request.get_json()
        # target_ip = body_json['target']
        # return r.id
    except Exception as e:
        print(e)
        exit(1)


# @app.route('/process/scanner/vulnerability', methods=["POST"])
# def process_scanner_vulnerability():
#     try:
#         body_json = request.get_json()
#         target_ip = body_json['target']
#         # scanner_service = Scanner(host=target_ip)
#         r = q.enqueue_call(scanner_service.scanner_async, result_ttl=500)
#         return r.id
#     except Exception as e:
#         print(e)
#         exit(1)


# @app.route('/process/cve/info', methods=["POST"])
# def process_cve_info():
#     try:
#         body_json = request.get_json()
#         target_cve = body_json['cve']
#         cve_search = seach_cve(cve=target_cve)
#         print(cve_search)
#         return jsonify(cve_search), 200
#     except Exception as e:
#         print(e)
#         # return jsonify({"status": "Not found"}), 404


@app.route('/result/<id>', methods=["POST"])
def result(id):
    try:
        job = q.fetch_job(id)
        if job.is_finished:
            return jsonify({"status": job.result}), 200
        else:
            return jsonify({"status": "pending"}), 202
    except:
        return jsonify({"status": "Not found"}), 404


if __name__ == '__main__':
    app.run()
