# import datetime
# import json
# import nmap
#
#
# # def connect_mongo():
# #     with open('setting/config.json', 'r') as f:
# #         config_json = json.load(f)
# #     db_scanner = config_json["database"]["scanner"]["base"]
# #     collection_scanner = config_json["database"]["scanner"]["collection"]
# #     connect = omicron_server.RecordMongo(db=db_scanner, coll=collection_scanner)
# #     return connect
#
#
# def callback_result(host, scan_result):
#     """
#
#     :param host:
#     :param scan_result:
#     :return:
#     """
#     try:
#         connect_mongo().database_scanner(host=host, scan_result=scan_result)
#         connect_mongo().close_connection()
#     except Exception as e:
#         status = "error: {}".format(e)
#         return status
#
#
# class Scanner(object):
#
#     def __init__(self, mac=None, arguments='-sV --host-timeout 10m', ports='1-65535'):
#         """
#
#         :param mac:
#         :param arguments:
#         :param ports:
#         """
#         self.mac = mac
#         self.arguments = arguments
#         self.ports = ports
#
#     def scanner(self, host):
#         """
#
#         :return:
#         """
#         try:
#             nm = nmap.PortScanner()
#             nm.scan(hosts=host, ports=self.ports, arguments=self.arguments)
#             result = {"ip": host, "mac": self.mac, "result": []}
#             i = 0
#             for host in nm.all_hosts():
#                 result["result"].append({"state": str(nm[host].state()),
#                                          "ports": []})
#                 for proto in nm[host].all_protocols():
#                     lport = nm[host][proto].keys()
#                     for port in lport:
#                         result["result"][i][int("ports")].append({'protocol': proto,
#                                                                   'port': port,
#                                                                   'state': nm[host][proto][port]['state'],
#                                                                   'name': nm[host][proto][port]['name'],
#                                                                   'cpe': nm[host][proto][port]['cpe'],
#                                                                   'version': nm[host][proto][port]['version'],
#                                                                   'product': nm[host][proto][port]['product']})
#                 i = i + 1
#             json_str = json.dumps(result, indent=4)
#             return json_str
#         except Exception as error:
#             print(error)
#             exit(1)
#
#     def scanner_async(self, full_scan, target=""):
#         """
#
#         :param full_scan:
#         :param target:
#         :return:
#         """
#         try:
#             ips = []
#             if full_scan:
#                 for host in connect_mongo().find():
#                     ips.append(host["ip"])
#                 connect_mongo().close_connection()
#             else:
#                 ips.append(target)
#             for ip in ips:
#                 nma = nmap.PortScannerAsync()
#                 nma.scan(hosts=ip, arguments=self.arguments, callback=callback_result)
#                 now = datetime.datetime.now()
#                 while nma.still_scanning():
#                     time_delta_sec = datetime.datetime.now() - now
#                     print("Waiting ... {0} sec.".format(time_delta_sec.seconds))
#                     nma.wait(60)
#             status = "success"
#             return status
#         except Exception as e:
#             status = "error: {}".format(e)
#             return status
