from itertools import groupby
from app import db_collection, db_scanner, get_config
from app.database import Inventory_Data_All


def chart_dashboard():
    """
    функция для агрегации данных по построению графиков на вкладке /dashboard
    Графики: port, service
    Таблицы: Last Task, Last CVE
    :return: список данных
    """
    ip_list = Inventory_Data_All()
    top_ports_list = []
    top_services_list = []
    top_vuln_list = []
    for i in ip_list:
        result_vulnerability = db_scanner.result.find({"host": i["ip"]}).sort("_id", -1).limit(1)
        for scanner in result_vulnerability:
            for result in scanner["open_port"]:
                top_ports_list.append(result["port"])
                top_services_list.append(result["name"])
            # for vuln in scanner["open_port"]:
            #     for vuln_cve in vuln["vulnerability"]["cve_mitre"]:
            #         top_vuln_list.append(vuln_cve["cve"])
    r_port = groupby(sorted(top_ports_list))
    r_service = groupby(sorted(top_services_list))
    # count_vuln = len(set(list(top_vuln_list)))
    count_vuln=0
    top_ports = top(top_ports_list, r_port)
    top_services = top(top_services_list, r_service)

    return ip_list, count_vuln, top_ports, top_services


def top(list_top, val):
    """
    создание массива данных (пример: [[ssh, 23],[http, 10]])
    :param list_top: список
    :param val: значение
    :return: отсортированный массив данных
    """
    res_sort = []
    for k, g in val:
        persent_port = (int(len(list(g))) * 100) / int(len(list_top))
        res_sort.append([k, round(persent_port, 2)])
    res_result = sorted(res_sort, key=lambda x: x[1], reverse=True)
    return res_result


def new_vulnerability():
    """
    функция возвращает список последних издексов CVE из базы данных
    :return: список последних CVE в базе данных
    """
    return db_collection.find().sort("_id", -1).limit(3)

# client = MongoClient()
config_json = get_config()
collection_info = db_scanner['vulnerability']


def find_cve(cve):
    return db_collection.find_one({"cve": cve})


def find_vulnerability(task):
    list_mng = []
    result_vulnerability = db_scanner.result.find({"uuid": task})
    # print(result_vulnerability)
    count_vulnerability = 0
    count_exploit = 0
    avg_cvss = 0.0
    result_avg_cvss = 0.0
    for vulnerability in result_vulnerability:
    #     for count_vuln in vulnerability:
    #         count_vulnerability = count_vulnerability + len(count_vuln['vulnerability']['cve_mitre'])
    #         for cvss in count_vuln['vulnerability']['cve_mitre']:
    #             # print(cvss['CVSS Score'])
    #             result_avg_cvss = float(result_avg_cvss) + float(cvss['CVSS Score'])
        print(vulnerability)
        list_mng.append(vulnerability)
    # # print(count_vulnerability)
    # if count_vulnerability > 0:
    #     result_avg_cvss = result_avg_cvss / count_vulnerability
    # else:
    #     result_avg_cvss = 0
    return list_mng, count_vulnerability, count_exploit, result_avg_cvss


def count_vulnerabity(ip):
    result_vulnerability = collection_info.find(ip)
    # count = 0
    # for i in result_vulnerability:
    #     count = count + 1
    return result_vulnerability
