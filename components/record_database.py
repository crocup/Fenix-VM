import datetime
import json
import pymongo


class RecordMongo(object):

    def __init__(self, db, coll, login=None, password=None):
        """

        :param db:
        :param coll:
        :param login:
        :param password:
        """
        self.conn = pymongo.MongoClient()
        self.login = login
        self.password = password
        self.db = self.conn[str(db)]
        self.coll = self.db[str(coll)]

    def database_inventory(self, result, date_now):
        """
        update or upsert data in mongo db
        :param result: list ip address
        :param date_now: format date and time
        :return: None
        """
        for data in result:
            ips_hostname = {"ip": data}
            sets = {"$set": {
                "date_update": date_now.strftime("%d-%m-%Y %H:%M")
            }}
            self.coll.update_one(ips_hostname, sets, upsert=True)

    def database_vulner(self, name_json):
        """

        :param name_json:
        :return:
        """
        with open('json/' + str(name_json), 'r', encoding='utf-8') as fh:
            data = json.load(fh)
        for datas in data["CVE_Items"]:
            cve = {"cve": datas["cve"]["CVE_data_meta"]["ID"]}
            data = {"$set": {
                "value": datas["cve"]["description"]["description_data"][0]["value"],
                "impact": datas["impact"],
                "lastModifiedDate": datas["lastModifiedDate"],
                "publishedDate": datas["publishedDate"],
                "configurations": datas["configurations"]
            }}
            self.coll.update_one(cve, data, upsert=True)

    def database_scanner(self, host, scan_result):
        """

        :param host:
        :param scan_result:
        :return:
        """
        ips_hostname = {"ip": str(host)}
        res = json.dumps(scan_result["scan"][host])
        result_json = json.loads(res)
        now = datetime.datetime.now()
        sets = {"$set": {
            "result_scan": result_json,
            "last_update": now.strftime("%d-%m-%Y %H:%M")
        }}
        return self.coll.update_one(ips_hostname, sets, upsert=True)

    def database_vulner_search_tcp(self, ip, time, port, cve, exploit_software, exploit_cpe):
        """

        :param ip:
        :param time:
        :param port:
        :param cve:
        :param exploit_software:
        :param exploit_cpe:
        :return:
        """
        ips_hostname = {"ip": ip}
        sets = {"$set": {
            "last_update": time.strftime("%d-%m-%Y %H:%M"),
            'result_scan.tcp.' + str(port) + '.cve': cve,
            'result_scan.tcp.' + str(port) + '.exploit_by_software': exploit_software,
            'result_scan.tcp.' + str(port) + '.exploit_by_cpe': exploit_cpe}}
        # json.dumps(sets)
        return self.coll.update_one(ips_hostname, sets, upsert=True)

    def close_connection(self):
        """

        :return:
        """
        return self.conn.close()

    def find_ip(self, ip):
        """

        :param ip:
        :return:
        """
        return self.coll.find_one({"ip": ip})
