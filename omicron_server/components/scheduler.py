import omicron_server


class SchedulerScanner(object):

    def __init__(self, target_mask):
        self.target_mask = target_mask

    def inventory_scheduler(self):
        """

        :return:
        """
        omicron_server.log.info("scheduler inventory-service start")
        inventory_service = omicron_server.Inventory(target=self.target_mask)
        inventory_service.result_scan()
        omicron_server.log.info("scheduler inventory-service stop")

    def full_scan_scheduler(self):
        """

        :return:
        """
        omicron_server.log.info("scheduler full scanner-service start")
        omicron_server.full_scan(target=self.target_mask)
        omicron_server.log.info("scheduler full scanner-service stop")
