import datetime
import json
import pymongo


class RecordMongo(object):

    def __init__(self, db, coll, login=None, password=None):
        """

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
            # check data in database
            ips = {"ip": data}
            result_check = self.coll.find_one(ips)
            ips_hostname = ips
            if result_check is None:
                tags = "None"
            else:
                tags = result_check["tags"]
            sets = {"$set": {
                "date_update": date_now.strftime("%d-%m-%Y %H:%M"),
                "tags": tags
            }}
            self.coll.update_one(ips_hostname, sets, upsert=True)

    def database_vulner(self, name_json):
        """

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

        """
        ips_hostname = {"ip": str(host)}
        res = json.dumps(scan_result["scan"][host])
        result_json = json.loads(res)
        now = datetime.datetime.now()
        sets = {"$set": {
            "result_scan": result_json,
            "last_update": now.strftime("%d-%m-%Y %H:%M")
        }}
        self.coll.update_one(ips_hostname, sets, upsert=True)

    def close_connection(self):
        """

        """
        self.conn.close()
