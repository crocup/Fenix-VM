import os
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
import logging.config
from components.inventory import Inventory
from components.scanner import Scanner
from components.full_scan import full_scan

app = Flask(__name__)
q = Queue(connection=Redis(), default_timeout=3600)

log_path = "logs/"
if not os.path.exists(log_path):
    os.mkdir(log_path)
setting_path = "settings/"
if not os.path.exists(setting_path):
    os.mkdir(setting_path)

# create the logging file handler
logging.config.fileConfig("settings/log.conf")
log = logging.getLogger("SpotterApp")


@app.route('/api/v1/process/inventory/start', methods=["POST"])
def process_inventory():
    try:
        log.info("inventory service start")
        body_json = request.get_json()
        target_mask = body_json['target']
        inventory_service = Inventory(target=target_mask)
        results = q.enqueue_call(inventory_service.result_scan, result_ttl=500)
        return results.id
    except Exception as e:
        log.error(e)
        exit(0)


@app.route('/api/v1/process/scanner/ip/start', methods=["POST"])
def process_scanner_ip():
    try:
        log.info("scanner service start")
        body_json = request.get_json()
        target_ip = body_json['target']
        scanner_service = Scanner(host=target_ip)
        results = q.enqueue_call(scanner_service.scanner_async, result_ttl=500)
        return results.id
    except Exception as e:
        log.error(e)
        exit(0)


@app.route('/api/v1/process/scanner/full/start', methods=["POST"])
def process_scanner_full():
    try:
        log.info("full scanner start")
        body_json = request.get_json()
        target_ip = body_json['target']
        results = q.enqueue_call(full_scan, args=(target_ip,), result_ttl=500)
        return results.id
    except Exception as e:
        log.error(e)
        exit(0)


@app.route('/api/v1/result/<id>', methods=["POST"])
def result(id):
    try:
        job = q.fetch_job(id)
        if job.is_finished:
            return jsonify({"status": job.result}), 200
        else:
            return jsonify({"status": "pending"}), 202
    except:
        log.error("Not found")
        return jsonify({"status": "Not found"}), 404


if __name__ == '__main__':
    app.run()
