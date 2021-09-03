from flask import Blueprint, jsonify, request, abort
from rq.job import Job
from fsec import q, conn
from fsec.modules.hostdiscovery.hostdiscovery import result_scanner, HostDiscovery

hostdiscovery = Blueprint('hostdiscovery', __name__)


@hostdiscovery.route('/api/v1/host/discovery/', methods=['POST'])
def hdiscovery_index():
    """

    """
    if not request.json or not 'host' in request.json:
        abort(400)
    data = request.get_json()
    job = q.enqueue_call(
        func=result_scanner, args=(HostDiscovery(data["host"]),), result_ttl=500
    )
    return jsonify(success=True, id=job.id)


@hostdiscovery.route("/api/v1/host/discovery/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return "waiting...", 202
