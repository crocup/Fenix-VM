import omicron_server
import schedule
import time


def run_scheduler():
    # print("------------------------start-------------------------")
    # run scheduler
    target_ips = omicron_server.config.get("NETWORK_IP", "IP")
    # time in hours
    sched_inventory = omicron_server.config.get("SCHEDULER", "INVENTORY")
    sched_full_scanner = omicron_server.config.get("SCHEDULER", "FULL_SCAN")
    sched = SchedulerScanner(target_mask=target_ips)
    # schedule.every(10).seconds.do(sched.inventory_scheduler)
    schedule.every(sched_inventory).hours.do(sched.inventory_scheduler)
    schedule.every(sched_full_scanner).hours.do(sched.full_scan_scheduler)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


class SchedulerScanner(object):

    def __init__(self, target_mask):
        self.target_mask = target_mask

    def inventory_scheduler(self):
        """

        :return:
        """
        print("------------------------start-------------------------")
        inventory_service = omicron_server.Inventory(target=self.target_mask)
        inventory_service.result_scan()

    def full_scan_scheduler(self):
        """

        :return:
        """
        omicron_server.full_scan(target=self.target_mask)
