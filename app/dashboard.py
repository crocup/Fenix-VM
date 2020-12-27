from pprint import pprint

from app import db_collection


def top_port():
    pass


def top_service():
    pass


def top_cve():
    pass


def new_vulnerability():
    result_cve = db_collection.find().sort("_id", -1).limit(3)
    # for i in result_cve:
    #     pprint(i)
    return result_cve


def last_login():
    pass
