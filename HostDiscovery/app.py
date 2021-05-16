"""
Сервис для обнаружения хостов в сети
Dmitry Livanov, 2021
ver 0.0.3
"""
from flask import Flask, request, abort, jsonify
from rq.job import Job
import configs
from task import get_hosts
from rq import Queue
from worker import conn
import os
from dotenv import load_dotenv

host_discovery = Flask(__name__)
host_discovery.config.from_object(configs.DevelopmentConfig)
q = Queue(name='discovery', connection=conn)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


@host_discovery.route('/api/v1/discovery/get', methods=['POST'])
def get_task():
    """

    :return:
    """
    if not request.json or not 'host' in request.json:
        abort(400)
    data = request.json
    job = q.enqueue_call(
        func=get_hosts, args=(data['host'],), result_ttl=500
    )
    return jsonify({"job": job.id})


@host_discovery.route("/api/v1/discovery/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return "waiting...", 202


if __name__ == '__main__':
    host_discovery.run(host='0.0.0.0', port=9001)
