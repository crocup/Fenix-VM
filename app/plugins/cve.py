# Описание
# Dmitry Livanov 2021
import json
import re
from typing import Dict, List
import requests
from bs4 import BeautifulSoup


def parse_html(link, product) -> list:
    """

    :param link:
    :param product:
    :return:
    """
    r = requests.get(link)
    soup = BeautifulSoup(r.text, "html.parser").find('div', id='TableWithRules')
    listing_item_main = soup.find_all('tr')
    list_result = []
    for i in listing_item_main:
        hr = i.find_data_all('td')
        list_array = [h.text for h in hr]
        if len(list_array) > 0 and re.search(str(product), list_array[1]):
            list_result.append(list_array[0])
    return list_result


class CVE_MITRE:

    def __init__(self, product, version):
        self.product = product
        self.version = version
        self.base_url = "https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword="

    def search(self) -> Dict:
        """

        :return:
        """
        product = str(self.product).split()
        line = product[0] + "+" + self.version
        line = line.replace(' ', '+')
        url = self.base_url + line
        dict_list = parse_html(link=url, product=product[0])
        print(dict_list)
        return json.loads(json.dumps({'cve_mitre': dict_list}))

    def result_data(self) -> List:
        """

        :return:
        """
        res = self.search()
        print(res)
        mitre_cve_array = []
        if res is not None:
            for list_cve in res['cve_mitre']:
                result = find_cve(list_cve)
                if result is None:
                    continue
                cvss_score = 0
                if 'impact' in result:
                    if 'baseMetricV2' in result['impact']:
                        cvss_score = result['impact']['baseMetricV2']['cvssV2']['baseScore']
                mitre_cve_list = {'cve': list_cve,
                                  'value': result['value'],
                                  'CVSS Score': cvss_score
                                  }
                mitre_cve_array.append(mitre_cve_list)
        print(mitre_cve_array)
        return mitre_cve_array
