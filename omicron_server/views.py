import json
import omicron_server
from omicron_server import app


@app.route('/api/v1/process/inventory/start', methods=["POST"])
def process_inventory():
    try:
        omicron_server.logger.info("inventory-service start")
        # open config file
        with open('setting/config.json', 'r') as f:
            config_json = json.load(f)
        target_mask = config_json["network"]["ip"]
        body_json = omicron_server.request.get_json()
        ping = body_json['ping']
        inventory_service = omicron_server.Inventory(target=target_mask)
        results = omicron_server.q.enqueue_call(inventory_service.result_scan, args=(ping,), result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/process/inventory/add', methods=["POST"])
def process_inventory_add():
    try:
        body_json = omicron_server.request.get_json()
        target_inventory = body_json['target']
        inventory_service = omicron_server.Inventory(target=target_inventory)
        inventory_add_scan = inventory_service.adding_scan_inventory()
        return omicron_server.jsonify(result=inventory_add_scan)
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/process/scanner/start', methods=["POST"])
def process_scanner_ip():
    """

    :return:
    """
    try:
        omicron_server.logger.info("scanner-service start")
        body_json = omicron_server.request.get_json()
        full_scan = body_json['full_scan']
        target = body_json['target']
        scanner_service = omicron_server.Scanner()
        results = omicron_server.q.enqueue_call(scanner_service.scanner_async,
                                                args=(full_scan, target,), result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/result/<uuid>', methods=["POST"])
def result(uuid):
    """

    :param uuid:
    :return:
    """
    try:
        job = omicron_server.q.fetch_job(uuid)
        if job.is_finished:
            return omicron_server.jsonify({"status": job.result}), 200
        else:
            return omicron_server.jsonify({"status": "pending"}), 202
    except Exception as e:
        omicron_server.logging.error("Error: Not found! {0}".format(e))
        return omicron_server.jsonify({"status": "Not found"}), 404


@app.route('/api/v1/process/vulnerability/start/cve', methods=["POST"])
def search_cve():
    """
    Example:
    json:
    target: "CVE-2017-0012"
    :return:
    """
    try:
        body_json = omicron_server.request.get_json()
        target_vulnerability_cve = body_json['cve']
        results = omicron_server.search_cve_details(target_vulnerability_cve)
        return results
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/process/vulnerability/search', methods=["POST"])
def search_v():
    """

    :return:
    """
    try:
        results = omicron_server.q.enqueue_call(omicron_server.full_search, result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)
