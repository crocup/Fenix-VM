from pymongo import MongoClient
from onicron import get_config

client = MongoClient()
config_json = get_config()

db = client['vulndb']
collection = db['cve']


def find_cve(cve):
    return collection.find_one({"cve": cve})
