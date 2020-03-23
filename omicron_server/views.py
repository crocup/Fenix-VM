import omicron_server
from omicron_server import app


def get_json():
    """
    :return:
    """
    body_json = omicron_server.request.get_json()
    target = body_json['target']
    return target


@app.route('/api/v1/process/inventory/start', methods=["POST"])
def process_inventory():
    try:
        omicron_server.logger.info("inventory-service start")
        target_mask = omicron_server.config.get("NETWORK_IP", "IP")
        inventory_service = omicron_server.Inventory(target=target_mask)
        results = omicron_server.q.enqueue_call(inventory_service.result_scan, result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/process/scanner/ip/start', methods=["POST"])
def process_scanner_ip():
    try:
        omicron_server.logger.info("scanner-service start")
        target_ip = get_json()
        scanner_service = omicron_server.Scanner(host=target_ip)
        results = omicron_server.q.enqueue_call(scanner_service.scanner_async, result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/process/scanner/full/start', methods=["POST"])
def process_scanner_full():
    try:
        omicron_server.logger.info("full-scanner-service start")
        target_ip = omicron_server.config.get("NETWORK_IP", "IP")
        results = omicron_server.q.enqueue_call(omicron_server.full_scan, args=(str(target_ip),), result_ttl=500)
        return results.id
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)


@app.route('/api/v1/result/<uuid>', methods=["POST"])
def result(uuid):
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
def search_vulners():
    """
    Example:
    json:
    target: "CVE-2017-0012"
    :return:
    """
    try:
        omicron_server.logger.info("search-vulners-service start")
        target_vulnerability_cve = get_json()
        results = omicron_server.vulnerabilities_api.get_cve(target_vulnerability_cve)
        return results
    except Exception as e:
        omicron_server.logging.error(e)
        exit(0)

