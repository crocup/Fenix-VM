from flask import Blueprint, render_template, redirect, url_for, jsonify, request, make_response
from flask_login import login_required, current_user
from . import get_config, logger
from redis import Redis
from rq import Queue
from app.inventory import Inventory
from app.result import log_file
from app.vulnerability.cve import *
from app.scanner import Scanner
from app.database import *
from .dashboard import new_vulnerability, chart_dashboard
from .notification import notification_message, delete_notification

q = Queue(connection=Redis(), default_timeout=86400)
main = Blueprint('main', __name__)


@main.app_errorhandler(404)
@login_required
def handle404(e):
    return render_template('404.html')


@main.route('/')
def index():
    return redirect(url_for('auth.login'))


@main.route('/about')
@login_required
def about():
    return render_template('about.html')


@main.route('/setting', methods=['GET', 'POST'])
@login_required
def setting():
    if request.method == 'POST':
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
        with open('config.json', 'w') as f:
            json.dump(config_json, f, indent=4)
    config_json_setting = get_config()
    return render_template('setting.html', ips=config_json_setting['network']['ip'],
                           api=config_json_setting['vulners']['api'],
                           interface=config_json_setting["network"]["interface"],
                           inventory=config_json_setting['scheduler']['inventory'],
                           scanner=config_json_setting['scheduler']['scanner'],
                           cve=config_json_setting['scheduler']['cve']
                           )


def host_discovery():
    config_json = get_config()
    target_mask = config_json["network"]["ip"]
    inventory_service = Inventory(target=target_mask)
    results_inventory = q.enqueue_call(inventory_service.result_scan, result_ttl=86400)
    return results_inventory


@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    if request.method == 'POST':
        host_discovery()
        # Result_Data(uid=results_inventory.id, name='Host Discovery', time=time())
        return render_template('inventory.html', items=Inventory_Data_All())
    else:
        return render_template('inventory.html', items=Inventory_Data_All())


@main.route('/inventory/<ip>', methods=['GET', 'POST'])
@login_required
def tags(ip):
    res_ip = Inventory_Data_Filter_IP(ip)
    inventory_array_ip = []
    for ips in Scanner_Data_All():
        tag_ip = Inventory_Data_Filter_IP(ips[0])
        if ips[0] == ip:
            dict_inventory_ip = {
                'ip': ips[0],
                'tag': tag_ip['tag'],
                'date': ips[1],
                'uuid': ips[2]
            }
            inventory_array_ip.append(dict_inventory_ip)
    if request.method == 'POST':
        tag_get = request.form.get("tag")
        Inventory_Tag_Record(ip=res_ip['ip'], tag=tag_get)
        return redirect(url_for('main.inventory'))
    else:
        return render_template('tag.html', ips=res_ip, items=inventory_array_ip)


@main.route('/result')
@login_required
def result_task():
    return render_template('result.html',
                           items=ResultPost.query.all(),
                           logs=log_file('logs/logging.log')
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
    result_dashboard = chart_dashboard()
    dashboard_task = ResultPost.query.all()
    data = {
        "name": current_user.name,
        "count_inventory": len(result_dashboard[0]),
        "count_vulners": result_dashboard[1],
        "port": result_dashboard[2],
        "service": result_dashboard[3],
        "last_cve": new_vulnerability(),
        "last_task": dashboard_task[len(dashboard_task) - 3:]
    }
    return render_template('dashboard.html', data=data)


@main.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    global results
    config_json = get_config()
    target_mask = config_json["network"]["ip"]
    scan = Scanner_Data_All()
    arr_ip = []
    for ip in scan:
        tag_ip = Inventory_Data_Filter_IP(ip[0])
        dict_ip = {
            'ip': ip[0],
            'tag': tag_ip['tag'],
            'date': ip[1],
            'uuid': ip[2]
        }
        arr_ip.append(dict_ip)

    if request.method == 'POST':
        scanner_host = request.form.get("scanner_text")
        scanner_service = Scanner(host=scanner_host)
        results = q.enqueue_call(scanner_service.scan_service_version, result_ttl=500)
        Result_Data(uid=results.id, name='Scanner', host=scanner_host, time=time())
    return render_template('scanner.html', ips=target_mask, items=arr_ip)


@main.route('/scanner/<uuid>', methods=['GET'])
@login_required
def scanner_info(uuid):
    dct = Scanner_Data_Filter_UUID(uid=uuid)
    for dict_data in dct:
        dct = dict_data
        print(dct)
    result_vuln = find_vulnerability(task=uuid)
    return render_template('info.html', uid=dct, info_mng=result_vuln[0], cntV=result_vuln[1], cntE=0,
                           cntD=0, cntP=0, avgS=round(result_vuln[3], 2))


def get_cve(name_cve):
    cve_upper = str(name_cve).upper().replace(' ', '')
    cve_text_p = find_cve(cve_upper)
    return cve_text_p


@main.route('/cve', methods=['GET', 'POST'])
@login_required
def cve():
    if request.method == 'POST':
        cve_form_get = request.form.get('cve_text')
        logger.info(f"Found CVE: {cve_form_get}")
        if len(cve_form_get) == 0:
            return render_template('cve.html', cve_info="")
        cve_text_p = get_cve(cve_form_get)
        return render_template('cve.html', cve_info=cve_text_p)
    else:
        return render_template('cve.html')


@main.route('/scheduler', methods=['GET', 'POST'])
@login_required
def main_scheduller():
    if request.method == 'POST':
        return render_template('scheduler.html')
    else:
        return render_template('scheduler.html')


@main.route('/notification', methods=['GET', 'POST'])
@login_required
def notification():
    if request.method == 'POST':
        delete_notification()
    message = notification_message()
    return render_template('notification.html', items=message)


@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        return render_template('report.html')
    else:
        return render_template('report.html')
