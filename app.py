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
        r = q.enqueue_call(inventory_service.result_scan, result_ttl=3600)
        return r.id
    except Exception as e:
        print(e)
        exit(1)


@app.route('/process/scanner/ip/start', methods=["POST"])
def process_scanner():
    try:
        body_json = request.get_json()
        target_ip = body_json['target']
        scanner_service = Scanner(host=target_ip)
        r = q.enqueue_call(scanner_service.scanner_async, result_ttl=3600)
        return r.id
    except Exception as e:
        print(e)
        exit(1)


@app.route('/result/<id>', methods=["POST"])
def result(id):
    try:
        job = q.fetch_job(id)
        if job.is_finished:
            status = {"status": job.result}
            return json.dumps(status, ensure_ascii=False)
        else:
            return jsonify({"status": "pending"}), 202
    except:
        return jsonify({"status": "Not found"}), 404


if __name__ == '__main__':
    app.run()
