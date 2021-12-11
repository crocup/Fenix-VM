from typing import Dict
import nmap3
from datetime import datetime
from app.core.config import DATABASE_PORT, DATABASE_IP
from app.core.scanner import AbstractScanner
from app.services.database import MessageProducer, MongoDriver


class HostDiscovery(AbstractScanner):
    """Only host discover (-sn)"""

    def scanner(self, host) -> Dict:
        """
        """
        return nmap3.NmapHostDiscovery().nmap_no_portscan(host)

    def del_misc_data(self, data) -> Dict:
        """
        """
        try:
            if "stats" in data:
                del data["stats"]
            if "runtime" in data:
                del data["runtime"]
        except Exception as e:
            data = {}
        return data

    def send_to_db(self, result):
        """
        """
        message_host_discovery = MessageProducer(MongoDriver(host=DATABASE_IP, port=DATABASE_PORT,
                                                             base=self.db, collection=self.table))
        for host in result:
            new_value = {"macaddress": result[host]["macaddress"],
                         "hostname": result[host]["hostname"],
                         "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")}
            message_host_discovery.update_message(message={"host": host}, new_value=new_value)
            # data = {
            #     "host": host,
            #     "hostname": result[host]["hostname"],
            #     "macaddress": result[host]["macaddress"],
            #     "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")
            # }
            # data_ip = message_host_discovery.get_message({"host": str(host)})
            # if data_ip is None:
            #     message_host_discovery.insert_message(data)
            # else:
            #     message_host_discovery.update_message(message={"host": host},
            #                                           new_value={"macaddress": result[host]["macaddress"],
            #                                                      "hostname": result[host]["hostname"],
            #                                                      "time": datetime.now().strftime("%H:%M:%S %d.%m.%Y")})
