import omicron_server


def full_scan(network):
    """

    :param network:
    :return:
    """
    try:
        # inventory
        inventory_service = omicron_server.Inventory(target=network)
        inventory_service.result_scan(ping=True)
        # scanner
        scanner_service = omicron_server.Scanner()
        scanner_service.scanner_async(full_scan=True)
        # vulnerability
        omicron_server.full_search()
        status = "success"
        return status
    except Exception as e:
        status = "error: {}".format(e)
        return status
