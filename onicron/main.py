from flask import Blueprint, render_template, redirect, url_for, jsonify, request, make_response
from flask_login import login_required, current_user
from . import db, time
from redis import Redis
from rq import Queue
import json
from onicron.inventory import Inventory, data_delete
from .models import ResultPost, InventoryPost
from .result import last_result

q = Queue(connection=Redis(), default_timeout=500)
main = Blueprint('main', __name__)


@main.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('main.dashboard'))


@main.route('/about')
@login_required
def about():
    return render_template('about.html', name=current_user.name)


@main.route('/setting')
@login_required
def setting():
    with open('onicron/config.json', 'r') as f:
        config_json = json.load(f)
    return render_template('setting.html', name=current_user.name, ips=config_json['network']['ip'],
                           api=config_json['vulners']['api'])


@main.route('/setting', methods=['POST'])
@login_required
def setting_post():
    with open('onicron/config.json', 'r') as f:
        config_json = json.load(f)
    ips = request.form.get('text')
    api_s = request.form.get('api')
    config_json['network']['ip'] = ips
    config_json['vulners']['api'] = api_s
    with open('onicron/config.json', 'w') as f:
        json.dump(config_json, f, indent=4)
    with open('onicron/config.json', 'r') as f:
        config_json = json.load(f)
    return render_template('setting.html', name=current_user.name, ips=config_json['network']['ip'],
                           api=config_json['vulners']['api'])


@main.route('/inventory')
@login_required
def inventory():
    res_uuid = result(last_result())
    return render_template('inventory.html', name=current_user.name, uid=res_uuid, items=InventoryPost.query.all())


@main.route('/inventory', methods=['POST'])
@login_required
def inventory_post():
    with open('onicron/config.json', 'r') as f:
        config_json = json.load(f)
    target_mask = config_json["network"]["ip"]
    traget_interface = config_json["network"]["interface"]
    inventory_service = Inventory(target=target_mask, interface=traget_interface)
    results = q.enqueue_call(inventory_service.result_scan, result_ttl=500)
    # record result.id in table
    res_id = ResultPost(results.id, 'Inventory', time())
    db.session.add(res_id)
    db.session.commit()
    return render_template('inventory.html', name=current_user.name, uid=results.id, items=InventoryPost.query.all())


@main.route('/inventory/delete/<ips>')
@login_required
def inventory_delete(ips):
    data_delete(ips)
    return redirect(url_for('main.inventory'))


@main.route('/result')
@login_required
def result_task():
    return render_template('result.html', name=current_user.name, items=ResultPost.query.all())


@main.route('/result/<uuid>')
@login_required
def result(uuid):
    try:
        job = q.fetch_job(uuid)
        if job.is_finished:
            return make_response(jsonify({"status": job.result}), 200).json['status']
        else:
            return make_response(jsonify({"status": "pending"}), 202).json['status']
    except Exception:
        return make_response(jsonify({"status": ""}), 404).json['status']


@main.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)


@main.route('/scanner')
@login_required
def scanner():
    return render_template('scanner.html', name=current_user.name)


@main.route('/cve')
@login_required
def cve():
    return render_template('cve.html', name=current_user.name)
