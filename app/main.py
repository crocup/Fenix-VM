"""
Flask
API приложения Fenix Security Scanner
Dmitry Livanov, 2021
"""
from bson import ObjectId
from flask import Blueprint, render_template, redirect, url_for, jsonify, request, make_response, send_from_directory, \
    abort
from flask_login import login_required
from . import logger
from redis import Redis
from rq import Queue
from app.config import *
from app.result import log_file
from .dashboard import find_vulnerability, dashboard_data
from .notification import notification_message
from .plugins.KB import table_KB, get_cve_info
from .plugins.info import *
from .plugins.report import *
from .task import host_discovery_task, scan_task, scan_db_task, delete_data_host_discovery
from app.service.database import MessageProducer, MongoDriver

# Брокер сообщений RQ Worker, TTL=1 день
q = Queue(connection=Redis(), default_timeout=86400)
main = Blueprint('main', __name__)


@main.app_errorhandler(404)
@login_required
def handle404(e):
    """
    Реализация отображения страницы при получении ошибки 404
    """
    return render_template('404.html')


@main.route('/')
def index():
    """
    Отображение главной страницы
    Происходит переадресация на страницу входа
    """
    return redirect(url_for('auth.login'))


@main.route('/about')
@login_required
def about():
    """
    Отображение общей информации о ПО
    Название, версия, лицензия, наличие обновлений
    """
    return render_template('about.html')


@main.route('/setting', methods=['GET'])
@login_required
def setting():
    """
    Реализация страницы настойки
    setting_networks, setting_data: Подключения для работы с базой данных.
    items_setting, items_notification: Получение всех данных из соответствующий коллекций
    return: Отображение страницы настройки
    """
    setting_networks = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                   base="setting", collection="network"))
    setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                               base="setting", collection="notification"))
    return render_template('setting.html', settings=setting_networks.get_all_message(),
                           notification=setting_data.get_all_message())


@main.route('/setting/network', methods=['GET', 'POST'])
@login_required
def setting_network():
    """
    Добавление настроек сети. Метод добавления POST
    Сохранение данных осуществляется в БД Mongo
    Метод GET для отображения страницы настроек сети
    """
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
        setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                   base="setting", collection="network"))
        setting_data.update_message(message=name, new_value=data)
        return redirect(url_for('main.setting'))
    else:
        return render_template('network.html')


@main.route('/setting/notification', methods=['GET', 'POST'])
@login_required
def setting_notification():
    """
    Добавление настроек для оповещения. Метод добавления POST
    Сохранение данных осуществляется в БД Mongo
    Метод GET для отображения страницы оповещения
    Поддерживается возможность оповещения по email  и в telegram канал, при помощи бота
    telegram: bot api
    chat_id: id канала в Telegram
    email: email пользователя
    """
    if request.method == 'POST':
        telegram = request.form.get('telegram')
        chat_id = request.form.get('chat_id')
        email = request.form.get('email')
        data = {
            "telegram_bot_api": telegram,
            "telegram_chat_id": chat_id,
            "email": email,
        }
        setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                   base="setting", collection="notification"))
        setting_data.insert_message(message=data)
        return redirect(url_for('main.setting'))
    else:
        return render_template('network_notification.html')


@main.route('/setting/<col>/delete/<_id>', methods=['GET'])
@login_required
def setting_network_delete(_id, col):
    """
    удаление сведений из БД
    col: название колекции в БД
    _id: Идентификатор в БД
    """
    setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                               base="setting", collection=col))
    setting_data.delete_message({'_id': ObjectId(_id)})
    return redirect(url_for('main.setting'))


@main.route('/inventory', methods=['GET', 'POST'])
@login_required
def inventory():
    """
    Реализация страницы Host Discovery
    Отображение в таблице всех обнаруженных хостов в сети
    setting_data: Подключение к БД
    get_mask_ip: Получение всех сохраненных хостов в сети
    .... дописать
    """
    setting_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                               base="setting", collection="network"))
    host_discovery_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                      base="host_discovery", collection="result"))
    if request.method == 'POST':
        select = request.form.get('comp_select')
        host_discovery_task(host=select)
        return redirect(url_for('main.inventory'))
    else:
        return render_template('inventory.html', items=host_discovery_data.get_all_message(),
                               net=setting_data.get_all_message())


@main.route('/inventory/<ip>', methods=['GET', 'POST'])
@login_required
def tags(ip):
    """
    Отображение всех задач по сканированию, связанных с IP-адресом
    Возможность назначить тег для IP адреса, а также отметить как важный хост
    :param ip: ip-адрес хоста
    :return: переадресания лиюо отображение страницы
    """
    host_discovery_ip = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                    base="scanner", collection="result"))
    data_all = host_discovery_ip.get_message({"host": ip})
    host_discovery_tag = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                     base="host_discovery", collection="result"))
    data_tag = host_discovery_tag.get_message({"ip": ip})
    if request.method == 'POST':
        tag_get = request.form.get("tag")
        important = request.form.get('important')
        if important:
            important = True
        else:
            important = False
        host_discovery_post_tag = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                              base="host_discovery", collection="result"))
        host_discovery_post_tag.update_message({"ip": ip}, {"tag": tag_get, "important": important})
        return redirect(url_for('main.inventory'))
    else:
        return render_template('tag.html', ips=ip, items=data_all, tag_items=data_tag)


@main.route('/inventory/<ip>/delete', methods=["POST"])
@login_required
def delete_host(ip):
    """
    Удаление IP адреса и всей информации о нем
    :param ip: ip-адрес хоста
    :return: Переадресация на страницу Host Discovery
    """
    delete_data_host_discovery(host=ip)
    return redirect(url_for('main.inventory'))


@main.route('/result')
@login_required
def result_task():
    """
    История всех запущенных задач по сканированию,
    а также логов приложения
    :return: Отображение страницы с историей
    """
    task_all = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                           base="scanner", collection="task"))
    item = task_all.get_all_message()
    return render_template('result.html',
                           items=item,
                           logs=log_file('app/logs/logging.log')
                           )


@main.route('/result/<uuid>')
@login_required
def result(uuid):
    """
    Статус задачи, запущенной с помощью брокера сообщений RQ Worker
    Важно: В записях установлено время жизни (TTL), не больше 1 дня
    """
    try:
        job = q.fetch_job(uuid)
        if job.is_finished:
            return make_response(jsonify({"status": job.result}), 200).json['status']
        else:
            return make_response(jsonify({"status": "pending"}), 202).json['status']
    except Exception as e:
        logger.error(e)
        return make_response(jsonify({"status": ""}), 404).json['status']


@main.route('/dashboard')
@login_required
def dashboard():
    """
    Главная страница приложения
    Содержатся графики и сведения о количестве уязвимстей, эксплойтов,
    обнаруженных хостов
    vie_data: Dict всех параметров для отображения графиков
    """
    vie_data = dashboard_data()
    return render_template('dashboard.html', data=vie_data)


@main.route('/scanner', methods=['GET', 'POST'])
@login_required
def scanner():
    """
    Информация о задачах по сканированию.
    Информация содержится в таблице и включает в себя:
    Название задачи, хост и время запуска
    Метод POST: для запуска задачи по сканированию
    host_discovery_ip: Подключение к БД
    data_all: Список всех записей
    results: id задачи в RQ Worker
    scan_db_task: Запись в БД (нужно исправить)
    :return: Отображение страницы /scanner
    """
    host_discovery_ip = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                                    base="scanner", collection="result"))
    data_all = host_discovery_ip.get_all_message()
    if request.method == 'POST':
        scanner_host = request.form.get("scanner_text")
        results = q.enqueue_call(scan_task, args=(scanner_host,), result_ttl=500)
        scan_db_task(result=results.id, host=scanner_host)
    return render_template('scanner.html', ips='', items=data_all)


@main.route('/scanner/<uuid>', methods=['GET', 'POST'])
@login_required
def scanner_info(uuid: str):
    """
    Информация о задаче
    result_vuln: Поиск уязвимостей в соответствии с задачей(нужно исправить)
    Раздел следует доработать
    """
    vuln_data = dict()
    scanner_data = MessageProducer(MongoDriver(host=MONGO_HOST, port=MONGO_PORT,
                                               base="scanner", collection="result"))
    for dict_data in scanner_data.get_message(message={"uuid": uuid}):
        vuln_data = dict_data
    count_vuln = result_count_data(VulnerabilityInfo(uuid))
    return render_template('info.html', uid=vuln_data, info_mng=0, cntV=count_vuln["count"], cntE=0,
                           cntD=0, cntP=0, avgS=round(count_vuln["avg"], 2))


@main.route('/scanner/<uuid>/delete', methods=['POST'])
@login_required
def scanner_data_delete(uuid: str):
    delete_task(uuid=uuid)
    return redirect(url_for('main.scanner'))


@main.route('/cve', methods=['GET', 'POST'])
@login_required
def cve():
    """
    База знаний
    На текущий момент содержится база знаний уязвимостей CVE из БД Mitre
    В методе POST передается идентификатор CVE (например: СVE-2019-0012)
    """
    if request.method == 'POST':
        cve_form_get = request.form.get('cve_text')
        logger.info(f"Found CVE: {cve_form_get}")
        if len(cve_form_get) == 0:
            return render_template('cve.html', cve_info="")
        return render_template('cve.html', cve_info=get_cve_info(cve_form_get))
    else:
        return render_template('cve.html', items=table_KB())


@main.route('/vulnerability/<vuln>', methods=['GET', 'POST'])
@login_required
def vulnerability_data(vuln):
    """

    """
    return render_template('cve.html', cve_info=vulnerability_info(vuln))


@main.route('/scheduler', methods=['GET', 'POST'])
@login_required
def main_scheduller():
    """

    """
    if request.method == 'POST':
        return render_template('scheduler.html')
    else:
        return render_template('scheduler.html')


@main.route('/notification', methods=['GET'])
@login_required
def notification():
    """
    Отображение последних 10 оповещений:
        - Новые ip адреса
        - Новые открытые порты
        - Изменения по сравнению с последним сканированием
        - Новые уязвимости
    message: 10 последних данных из БД
    """
    message = notification_message()
    return render_template('notification.html', items=message)


@main.route('/report', methods=['GET', 'POST'])
@login_required
def report():
    """
    Отчеты в формате PDF
    Еще не реализовано....
    """
    return render_template('report.html', items=list_report())


@main.route('/report/<uuid>', methods=['POST'])
@login_required
def report_task(uuid):
    """
    Отчеты в формате PDF
    Еще не реализовано....
    """
    result_report(PDF_Report(), data=uuid)
    return render_template('report.html')


@main.route('/report/<name>/delete', methods=['POST'])
@login_required
def report_delete(name):
    """

    """
    del_report(name)
    return render_template('report.html')


@main.route('/report/<path:path>', methods=['GET'])
@login_required
def open_pdf(path):
    try:
        return send_from_directory(basedir + '/report/', filename=path, mimetype='application/pdf')
    except FileNotFoundError:
        abort(404)
