import datetime
import json
import logging.config
import nmap
import configparser
from components.record_database import RecordMongo

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
        record.close_connection()
        status = "success"
        return status
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
        except Exception as error:
            print(error)

    def scanner_yield(self):
        """

        :return:
        """
        nm = nmap.PortScannerYield()
        for progressive_result in nm.scan(self.host, self.ports):
            print(progressive_result)

    def scanner_dmz(self):
        pass
