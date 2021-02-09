"""
Сервис для загрузки базы CVE MITRE
Автор: Dmitry Livanov, 2020
"""
import json
import flask
import os
import requests
import wget
import zipfile
from app.service.cve.config import *

app = flask.Flask(__name__)
json_path = "json/"
if not os.path.exists(json_path):
    os.mkdir(json_path, 0o755)


def download(years):
    """
    download feeds cve
    :param years: finish year feeds
    :return: None
    """
    try:
        for year in range(2002, int(years)):
            name = 'nvdcve-1.1-' + str(year) + '.json.zip'
            name_json = 'nvdcve-1.1-' + str(year) + '.json'
            url = 'https://nvd.nist.gov/feeds/json/cve/1.1/' + str(name)
            wget.download(url, 'json/' + str(name))
            unzip(name)
            os.remove('json/' + str(name))
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
                data_upsert = {
                    "name": cve,
                    "set": data
                }
                requests.post(UPSERT_DATABASE, json={"data": data_upsert, "base": BASE, "collection": COLLECTION})
            os.remove('json/' + str(name_json))
    except Exception as e:
        print(e)


def unzip(name):
    """
    unzip feeds
    :param name: name zip file
    :return: None
    """
    try:
        cve_zip = zipfile.ZipFile('json/' + str(name))
        cve_zip.extractall('json/')
        cve_zip.close()
    except Exception as e:
        print(e)


@app.route('/api/v1/cve/mitre/download', methods=['POST'])
def download_data():
    download(years=YEAR)


if __name__ == '__main__':
    app.run(port=9002)
