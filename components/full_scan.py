from components.inventory import Inventory
from components.scanner import Scanner


def full_scan(target):
    try:
        inventory_service = Inventory(target=target)
        result_inventory = inventory_service.result_scan()
        for ips in result_inventory[1]:
            scanner_service = Scanner(host=ips)
            scanner_service.scanner_async()
        status = "success"
        return status
    except Exception as e:
        status = "error: {}".format(e)
        return status
