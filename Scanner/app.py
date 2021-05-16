"""
Сервис для обнаружения хостов в сети
Dmitry Livanov, 2021
ver 0.0.3
"""
from datetime import datetime

from flask import Flask, request, abort, jsonify
from rq.job import Job
import task
from rq import Queue
from worker import conn
import os
from dotenv import load_dotenv
import conf
from database import MessageProducer, MongoDriver

host_discovery = Flask(__name__)
host_discovery.config.from_object(conf.DevelopmentConfig)
q = Queue(name='scanner', connection=conn)

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def time():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time


@host_discovery.route('/api/v1/scanner/start', methods=['POST'])
def wscan():
    """

    :return:
    """
    if not request.json or not 'host' in request.json:
        abort(400)
    data = request.json
    job = q.enqueue_call(
        func=task.scanner_work, args=(data['host'],), result_ttl=500, timeout=500
    )
    data = {
        "uuid": job.id,
        "name": "Scanner",
        "host": data['host'],
        "time": time()
    }
    message_mongo = MessageProducer(MongoDriver(host=conf.Config.MONGO_HOST, port=conf.Config.MONGO_PORT,
                                                base="scanner", collection="task"))
    message_mongo.insert_message(data)
    return jsonify({"job": job.id})


@host_discovery.route("/api/v1/scanner/results/<job_key>", methods=['GET'])
def get_results(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        return str(job.result), 200
    else:
        return "waiting...", 202


if __name__ == '__main__':
    host_discovery.run(host='0.0.0.0', port=9101)
