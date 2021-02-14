from bson import ObjectId
from flask import Blueprint, render_template, redirect, url_for, jsonify, request, make_response
from flask_login import login_required
from . import logger
from redis import Redis
from rq import Queue
from app.result import log_file
from .dashboard import find_vulnerability
from .notification import notification_message
from app.service.database.database import Storage
from .task import host_discovery_task, scan_task, scan_db_task

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


@main.route('/setting', methods=['GET'])
@login_required
def setting():
    setting_data = Storage(db='setting', collection='network')
    items_setting = setting_data.find_data_all()

    setting_data = Storage(db='setting', collection='notification')
    items_notification = setting_data.find_data_all()
    return render_template('setting.html', settings=items_setting, notification=items_notification)


@main.route('/setting/network', methods=['GET', 'POST'])
@login_required
def setting_network():
    if request.method == 'POST':
        network = request.form.get('network')
        interface = request.form.get('interface')
        description = request.form.get('description')
        private = request.form.get('private')
        telegram = request.form.get('telegram')
        mail = request.form.get('mail')
        if private is None:
            private = "Open Network"
        else:
            private = "Private Network"
        name = {
            "network": network
        }
        data = {
            "interface": interface,
            "description": description,
            "private": private,
            "telegram": telegram,
            "mail": mail
        }
        setting_data = Storage(db='setting', collection='network')
        setting_data.upsert(name, data)
        return redirect(url_for('main.setting'))
    else:
        return render_template('network.html')


@main.route('/setting/notification', methods=['GET', 'POST'])
@login_required
def setting_notification():
    if request.method == 'POST':
        telegram = request.form.get('telegram')
        chat_id = request.form.get('chat_id')
        email = request.form.get('email')
        setting_data = Storage(db='setting', collection='notification')
        data = {
            "telegram_bot_api": telegram,
            "telegram_chat_id": chat_id,
            "email": email,
        }
        setting_data.insert(data)
        return redirect(url_for('main.setting'))
    else:
        return render_template('network_notification.html')


@main.route('/setting/<col>/delete/<_id>', methods=['GET'])
@login_required
def setting_network_delete(_id, col):
    setting_data = Storage(db='setting', collection=col)
    setting_data.delete({'_id': ObjectId(_id)})
    return redirect(url_for('main.setting'))


@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    """

    :return:
    """
    setting_data = Storage(db='setting', collection='network')
    get_mask_ip = setting_data.find_data_all()
    host_discovery_data = Storage(db='host_discovery', collection='result')
    item = host_discovery_data.find_data_all()
    if request.method == 'POST':
        select = request.form.get('comp_select')
        q.enqueue_call(host_discovery_task, args=(select,), result_ttl=500)
        return render_template('inventory.html', items=item, net=get_mask_ip)
    else:
        return render_template('inventory.html', items=item, net=get_mask_ip)


@main.route('/inventory/<ip>', methods=['GET', 'POST'])
@login_required
def tags(ip):
    """

    :param ip:
    :return:
    """
    # исправить ошибку с тегами
    host_discovery_ip = Storage(db='scanner', collection='result')
    data_all = host_discovery_ip.data_one({"host": ip})
    if request.method == 'POST':
        tag_get = request.form.get("tag")
        host_discovery_tag = Storage(db='host_discovery', collection='result')
        host_discovery_tag.update({"ip": ip}, {"tag": tag_get})
        return redirect(url_for('main.inventory'))
    else:
        return render_template('tag.html', ips=ip, items=data_all)


@main.route('/inventory/<ip>/delete', methods=["POST"])
@login_required
def delete_host(ip):
    """
    Удаление IP адреса и всей информации о нем
    :param ip: ip-адрес
    :return: None
    """
    # delete_ip(host=ip)  # удаление из sqlite
    # hosts_id = db_scanner['result']
    # hosts_id.delete_many({"host": ip})
    return redirect(url_for('main.inventory'))


@main.route('/result')
@login_required
def result_task():
    """

    :return:
    """
    task_all = Storage(db='scanner', collection='task')
    item = task_all.find_data_all()
    return render_template('result.html',
                           items=item,
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
    # result_dashboard = chart_dashboard()
    # dashboard_task = ResultPost.query.all()
    # data = {
    #     "name": current_user.name,
    #     "count_inventory": len(result_dashboard[0]),
    #     "count_vulners": result_dashboard[1],
    #     "port": result_dashboard[2],
    #     "service": result_dashboard[3],
    #     "last_cve": new_vulnerability(),
    #     "last_task": dashboard_task[len(dashboard_task) - 3:]
    # }
    return render_template('dashboard.html', data="")


@main.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    """

    :return:
    """
    host_discovery_ip = Storage(db='scanner', collection='result')
    data_all = host_discovery_ip.find_data_all()
    if request.method == 'POST':
        scanner_host = request.form.get("scanner_text")
        results = q.enqueue_call(scan_task, args=(scanner_host,), result_ttl=500)
        # запись в БД task
        scan_db_task(result=results.id, host=scanner_host)
    return render_template('scanner.html', ips='', items=data_all)


@main.route('/scanner/<uuid>', methods=['GET'])
@login_required
def scanner_info(uuid: str):
    dct = dict()
    scanner_data = Storage(db='scanner', collection='result')
    for dict_data in scanner_data.data_one(data={"uuid": uuid}):
        dct = dict_data
    result_vuln = find_vulnerability(task=uuid)
    return render_template('info.html', uid=dct, info_mng=result_vuln[0], cntV=result_vuln[1], cntE=0,
                           cntD=0, cntP=0, avgS=round(result_vuln[3], 2))


@main.route('/cve', methods=['GET', 'POST'])
@login_required
def cve():
    if request.method == 'POST':
        cve_form_get = request.form.get('cve_text')
        logger.info(f"Found CVE: {cve_form_get}")
        if len(cve_form_get) == 0:
            return render_template('cve.html', cve_info="")
        cve_upper = str(cve_form_get).upper().replace(' ', '')
        knowledge_base = Storage(db='vulndb', collection='cve')
        data = knowledge_base.data_one(data={"cve": cve_upper})
        return render_template('cve.html', cve_info=data)
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
    # if request.method == 'POST':
    #     delete_notification()
    message = notification_message()
    return render_template('notification.html', items=message)


@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    if request.method == 'POST':
        return render_template('report.html')
    else:
        return render_template('report.html')
