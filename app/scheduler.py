from app.main import q
from app.service.database.database import Storage
from app.task import host_discovery_task, scan_task, scan_db_task

setting_data = Storage(db='setting', collection='network')


def scheduler_host_discovery():
    """

    :return:
    """
    items = setting_data.find_data_all()
    for net in items:
        q.enqueue_call(host_discovery_task, args=(net["network"],), result_ttl=500)


def scheduler_scanner():
    """

    :return:
    """
    items = setting_data.find_data_all()
    for net in items:
        results = q.enqueue_call(scan_task, args=(net["network"],), result_ttl=500)
        scan_db_task(result=results.id, host=net["network"])
