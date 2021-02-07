from app import db_scanner


def dashboard_open_port():
    pass


def dashboard_service():
    pass


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


collection_info = db_scanner['vulnerability']


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
        #     print(vulnerability)
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
