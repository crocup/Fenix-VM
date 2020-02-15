import omicron_server
import schedule
from time import sleep


def run_scheduler():
    try:
        target_ips = omicron_server.config.get("NETWORK_IP", "IP")
        sched_inventory = omicron_server.config.get("SCHEDULER", "INVENTORY")
        sched_full_scanner = omicron_server.config.get("SCHEDULER", "FULL_SCAN")
        sched = SchedulerScanner(target_mask=target_ips)
        schedule.every(int(sched_inventory)).hours.do(sched.inventory_scheduler)
        schedule.every(int(sched_full_scanner)).hours.do(sched.full_scan_scheduler)
        while True:
            schedule.run_pending()
            sleep(1)
    except Exception as e:
        omicron_server.logger.error(e)


class SchedulerScanner(object):

    def __init__(self, target_mask):
        self.target_mask = target_mask

    def inventory_scheduler(self):
        """

        :return:
        """
        omicron_server.logger.info("start scheduler inventory")
        inventory_service = omicron_server.Inventory(target=self.target_mask)
        inventory_service.result_scan()

    def full_scan_scheduler(self):
        """

        :return:
        """
        omicron_server.logger.info("start scheduler full scanner")
        omicron_server.full_scan(target=self.target_mask)
