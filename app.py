import json
import logging.config
import os
from flask import Flask, request, jsonify
from redis import Redis
from rq import Queue
from components.inventory import Inventory

app = Flask(__name__)
q = Queue(connection=Redis(), default_timeout=3600)

log_path = "logs/"
if not os.path.exists(log_path):
    os.mkdir(log_path)
setting_path = "settings/"
if not os.path.exists(setting_path):
    os.mkdir(setting_path)

# create the logging file handler
logging.config.fileConfig('settings/log_inventory.conf')
log = logging.getLogger("InventoryService")


@app.route('/process/inventory/start', methods=["POST"])
def process():
    body_json = request.get_json()
    target_mask = body_json['target']
    inventory_service = Inventory(target=target_mask)
    r = q.enqueue_call(inventory_service.result_scan, result_ttl=300)
    return r.id


@app.route('/result/inventory/<id>', methods=["POST"])
def result(id):
    try:
        job = q.fetch_job(id)
        if job.is_finished:
            results = {"result": job.result}
            return json.dumps(results, ensure_ascii=False)
        else:
            return jsonify({"result": "pending"}), 202
    except:
        log.error("Not found")
        return jsonify({"result": "Not found"}), 404


if __name__ == '__main__':
    app.run()
