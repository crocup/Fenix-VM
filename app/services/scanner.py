from typing import Dict
import nmap3
from datetime import datetime
from app.core.config import DATABASE_IP, DATABASE_PORT
from app.core.scanner import AbstractScanner, result_scan
from app.services.database import MessageProducer, MongoDriver


class ServiceDetection(AbstractScanner):
    """ """

    def scanner(self, host) -> Dict:
        """
        """
        return nmap3.Nmap().nmap_version_detection(host)

    def del_misc_data(self, data) -> Dict:
        try:
            if "stats" in data:
                del data["stats"]
            if "runtime" in data:
                del data["runtime"]
        except Exception as e:
            data = {}
        return data

    def send_to_db(self, result):
        message_host_scanner = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                           base=self.db, collection=self.table))
        for host in result:
            data = {
                "host": host,
                "name": self.name,
                "result": result[host],
                "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")
            }
            message_host_scanner.insert_message(data)


if __name__ == "__main__":
    result_scan(ServiceDetection(host="192.168.1.1", name="test", db="Scanner", table="result"))
