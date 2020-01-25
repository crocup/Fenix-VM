import datetime
import json
import nmap
import configparser
from components.record_database import RecordMongo
from components.search_vulnerability import VulnerabilitySearch, search_circl

# read settings file
_path = "settings/settings_scanner.conf"
config = configparser.ConfigParser()
config.read(_path)


def callback_result(host, scan_result):
    """

    :param host:
    :param scan_result:
    :return:
    """
    try:
        record = RecordMongo(db=config.get("DATABASE_SCANNER", "BASE"),
                             coll=config.get("DATABASE_SCANNER", "COLLECTION"))
        record.database_scanner(host=host, scan_result=scan_result)
        result = record.find_ip(ip=host)
        vulnerabilities_api = VulnerabilitySearch(vulners_api=config.get("VULNERS", "API"))
        for port in result['result_scan']['tcp']:
            cpe = result['result_scan']['tcp'][port]['cpe']
            product = result['result_scan']['tcp'][port]['product']
            version = result['result_scan']['tcp'][port]['version']
            # Get now data
            now = datetime.datetime.now()
            # get CVE
            vulnerabilities_cve_list = search_circl(cpe=cpe)
            # Get vulnerabilities and exploits by software name and version
            vulnerabilities_exploit_list_software = vulnerabilities_api.get_vulnerabilities_by_software(name=product,
                                                                                                        version=version)
            # Get vulnerabilities by CPE product and version string
            vulnerabilities_exploit_list_cpe = vulnerabilities_api.get_vulnerabilities_by_cpe(cpe=cpe)
            record.database_vulner_search_tcp(ip=host, time=now, port=port,
                                              cve=vulnerabilities_cve_list,
                                              exploit_software=vulnerabilities_exploit_list_software,
                                              exploit_cpe=vulnerabilities_exploit_list_cpe)

        record.close_connection()
    except Exception as e:
        status = "error: {}".format(e)
        return status


class Scanner(object):

    def __init__(self, host, mac=None, arguments='-sV --host-timeout 15m', ports='1-65535'):
        """

        :param host:
        :param mac:
        :param arguments:
        :param ports:
        """
        self.host = host
        self.mac = mac
        self.arguments = arguments
        self.ports = ports

    def scanner(self):
        """

        :return:
        """
        try:
            nm = nmap.PortScanner()
            nm.scan(hosts=self.host, ports=self.ports, arguments=self.arguments)
            result = {"ip": self.host, "mac": self.mac, "result": []}
            i = 0
            for host in nm.all_hosts():
                result["result"].append({"state": str(nm[host].state()),
                                         "ports": []})
                for proto in nm[host].all_protocols():
                    lport = nm[host][proto].keys()
                    for port in lport:
                        result["result"][i][int("ports")].append({'protocol': proto,
                                                                  'port': port,
                                                                  'state': nm[host][proto][port]['state'],
                                                                  'name': nm[host][proto][port]['name'],
                                                                  'cpe': nm[host][proto][port]['cpe'],
                                                                  'version': nm[host][proto][port]['version'],
                                                                  'product': nm[host][proto][port]['product']})
                i = i + 1
            json_str = json.dumps(result, indent=4)
            return json_str
        except Exception as error:
            print(error)
            exit(1)

    def scanner_async(self):
        """

        :return:
        """
        try:
            nma = nmap.PortScannerAsync()
            nma.scan(hosts=self.host, arguments=self.arguments, callback=callback_result)
            now = datetime.datetime.now()
            while nma.still_scanning():
                time_delta_sec = datetime.datetime.now() - now
                print("Waiting ... {0} sec.".format(time_delta_sec.seconds))
                nma.wait(60)

            status = "success"
            return status
        except Exception as e:
            status = "error: {}".format(e)
            return status

    def scanner_yield(self):
        """

        :return:
        """
        nm = nmap.PortScannerYield()
        for progressive_result in nm.scan(self.host, self.ports):
            print(progressive_result)

    def scanner_dmz(self):
        pass
