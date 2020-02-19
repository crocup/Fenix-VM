import omicron_server


def full_scan(target):
    try:
        inventory_service = omicron_server.Inventory(target=target)
        result_inventory = inventory_service.result_scan()
        for ips in result_inventory[1]:
            scanner_service = omicron_server.Scanner(host=ips)
            scanner_service.scanner_async()
        status = "success"
        return status
    except Exception as e:
        status = "error: {}".format(e)
        return status


def full_scan_ip(ips):
    try:
        scanner_service = omicron_server.Scanner(host=ips)
        scanner_service.scanner_async()
        status = "success"
        return status
    except Exception as e:
        status = "error: {}".format(e)
        return status
