import requests
from app import db_scanner
from app.config import GET_ALL_DATABASE


def dashboard_data():
    """

    :return:
    """
    # count host
    data_all_host = requests.post(GET_ALL_DATABASE, json={"base": "host_discovery", "collection": "result"})
    count = data_all_host.json()
    # host discovery
    data = {
        "count_host": count["count"],
        "count_important_host": 2,
        "count_vulnerability": 43,
        "exploit": 2,
        "score": 4.7,
        "ports": [],
        "service": [],
        "task": [],
        "KB": []
    }
    return data


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


collection_info = db_scanner['plugins']


def find_vulnerability(task):
    list_mng = []
    result_vulnerability = db_scanner.result.find({"uuid": task})
    # print(result_vulnerability)
    count_vulnerability = 0
    count_exploit = 0
    avg_cvss = 0.0
    result_avg_cvss = 0.0
    for vulnerability in result_vulnerability:
        #     for count_vuln in plugins:
        #         count_vulnerability = count_vulnerability + len(count_vuln['plugins']['cve_mitre'])
        #         for cvss in count_vuln['plugins']['cve_mitre']:
        #             # print(cvss['CVSS Score'])
        #             result_avg_cvss = float(result_avg_cvss) + float(cvss['CVSS Score'])
        #     print(plugins)
        list_mng.append(vulnerability)
    # # print(count_vulnerability)
    # if count_vulnerability > 0:
    #     result_avg_cvss = result_avg_cvss / count_vulnerability
    # else:
    #     result_avg_cvss = 0
    return list_mng, count_vulnerability, count_exploit, result_avg_cvss


def count_vulnerabity(ip):
    result_vulnerability = collection_info.find(ip)
    return result_vulnerability
