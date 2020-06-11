from flask import Blueprint, render_template, redirect, url_for, jsonify, request, make_response
from flask_login import login_required, current_user
from . import db, time, get_config
from redis import Redis
from rq import Queue
import json
from app.inventory import Inventory, data_delete
from .models import ResultPost, InventoryPost
from .result import last_result
from .cve import find_cve

q = Queue(connection=Redis(), default_timeout=500)
main = Blueprint('main', __name__)


@main.app_errorhandler(404)
def handle404(e):
    return render_template('404.html', name=current_user.name), 404


@main.route('/')
def index():
    # return render_template('index.html')
    return redirect(url_for('auth.login'))


@main.route('/about')
@login_required
def about():
    return render_template('about.html', name=current_user.name)


@main.route('/setting')
@login_required
def setting():
    config_json = get_config()
    return render_template('setting.html',
                           name=current_user.name,
                           ips=config_json['network']['ip'],
                           api=config_json['vulners']['api'],
                           interface=config_json["network"]["interface"],
                           inventory=config_json['scheduler']['inventory'],
                           scanner=config_json['scheduler']['scanner'],
                           cve=config_json['scheduler']['cve']
                           )


@main.route('/setting', methods=['POST'])
@login_required
def setting_post():
    config_json = get_config()
    ips = request.form.get('text')
    interface = request.form.get('interface')
    api_s = request.form.get('api')
    inventory_p = request.form.get('inventory')
    scanner_p = request.form.get('scanner')
    cve_p = request.form.get('cve')
    config_json['network']['ip'] = ips
    config_json['network']['interface'] = interface
    config_json['vulners']['api'] = api_s
    config_json['scheduler']['inventory'] = inventory_p
    config_json['scheduler']['scanner'] = scanner_p
    config_json['scheduler']['cve'] = cve_p
    with open('app/config.json', 'w') as f:
        json.dump(config_json, f, indent=4)
    config_json = get_config()
    return render_template('setting.html',
                           name=current_user.name,
                           ips=config_json['network']['ip'],
                           api=config_json['vulners']['api'],
                           interface=config_json["network"]["interface"],
                           inventory=config_json['scheduler']['inventory'],
                           scanner=config_json['scheduler']['scanner'],
                           cve=config_json['scheduler']['cve']
                           )


@main.route('/inventory')
@login_required
def inventory():
    res_uuid = result(last_result())
    return render_template('inventory.html',
                           name=current_user.name,
                           uid=res_uuid,
                           items=InventoryPost.query.all()
                           )


@main.route('/inventory', methods=['POST'])
@login_required
def inventory_post():
    config_json = get_config()
    target_mask = config_json["network"]["ip"]
    traget_interface = config_json["network"]["interface"]
    inventory_service = Inventory(target=target_mask, interface=traget_interface)
    results = q.enqueue_call(inventory_service.result_scan, result_ttl=500)
    # record result.id in table
    res_id = ResultPost(results.id, 'Inventory', time())
    db.session.add(res_id)
    db.session.commit()
    return render_template('inventory.html',
                           name=current_user.name,
                           uid=results.id,
                           items=InventoryPost.query.all()
                           )


@main.route('/inventory/delete/<ips>')
@login_required
def inventory_delete(ips):
    data_delete(ips)
    return redirect(url_for('main.inventory'))


@main.route('/result')
@login_required
def result_task():
    return render_template('result.html',
                           name=current_user.name,
                           items=ResultPost.query.all()
                           )


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
    return render_template('dashboard.html',
                           name=current_user.name
                           )


@main.route('/scanner')
@login_required
def scanner():
    return render_template('scanner.html',
                           name=current_user.name
                           )


@main.route('/scanner', methods=['POST'])
@login_required
def scanner_post():
    return render_template('scanner.html',
                           name=current_user.name
                           )


@main.route('/cve')
@login_required
def cve():
    return render_template('cve.html', name=current_user.name)


@main.route('/cve', methods=['POST'])
@login_required
def cve_post():
    cve_form_get = request.form.get('cve_text')
    if len(cve_form_get) == 0:
        return render_template('cve.html', name=current_user.name, cve_info="")
    cve_upper = str(cve_form_get).upper().replace(' ', '')
    cve_text_p = find_cve(cve_upper)

    return render_template('cve.html',
                           name=current_user.name,
                           cve_info=cve_text_p
                           )


@main.route('/news')
@login_required
def news():
    return render_template('news.html', name=current_user.name)

