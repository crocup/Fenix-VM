"""
Клас для работы с базой данных Mongo
Dmitry Livanov, 2021
"""
import json
from pymongo import MongoClient
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class Storage(object):
    def __init__(self, db: str = None, collection: str = None):
        self.client_mongo = MongoClient()
        self.db = self.client_mongo[db]
        self.collection = collection

    def insert(self, data: dict = None):
        """
        :param data:
        :return:
        """
        return self.db[self.collection].insert_one(data)

    def update(self, name: dict = None, data: dict = None):
        """
        :param name:
        :param data:
        :return:
        """
        return self.db[self.collection].update_one(name, {"$set": data})

    def upsert(self, name: dict = None, data: dict = None):
        """
        :param name:
        :param data:
        :return:
        """
        return self.db[self.collection].update_one(name, {"$set": data}, upsert=True)

    def delete(self, name: dict = None):
        """
        :param name:
        :return:
        """
        return self.db[self.collection].delete_one(name)

    def find_data_all(self):
        return self.db[self.collection].find()

    def find_one(self, data: dict) -> str:
        result = ""
        for item in self.db[self.collection].find(data):
            result = item
        return JSONEncoder().encode(result)

    def data_one(self, data: dict):
        return self.db[self.collection].find(data)

    def delete_all(self):
        pass

    def close_connection(self):
        return self.client_mongo.close()