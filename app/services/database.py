from abc import ABC, abstractmethod
from typing import Dict
from pymongo import MongoClient
import logging
import json
from bson import ObjectId
from app.models.database import Message


class Driver(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def insert(self, message):
        pass

    @abstractmethod
    def delete(self, message):
        pass

    @abstractmethod
    def update(self, message, new_values):
        pass

    @abstractmethod
    def get_one(self, message):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def get_message_limit(self, count):
        pass

    @abstractmethod
    def count_doc(self, count):
        pass


class MongoDriver(Driver):
    def __init__(self, host, port, base, collection):
        self.client = MongoClient(host, port)
        self.base = self.client[base]
        self.collection = self.base[collection]

    def connect(self):
        self._conect_to_mongo()

    def _conect_to_mongo(self):
        logging.info('Connect to mongo')

    def disconnect(self):
        self._disconnect_from_mongo()

    def _disconnect_from_mongo(self):
        self.client.close()
        logging.info('Disconnect from mongo')

    def insert(self, message):
        return self._insert_message(message)

    def _insert_message(self, message):
        self.collection.insert_one(message)
        return Message(success=True)

    def delete(self, message):
        return self._delete_message(message)

    def _delete_message(self, message):
        try:
            self.collection.delete_one(message)
            return Message(success=True)
        except Exception as e:
            return Message(success=False)

    def update(self, message, new_value):
        return self._update_message(message, new_value)

    def _update_message(self, message, new_value):
        try:
            self.collection.update_one(message, {'$set': new_value}, upsert=True)
            return Message(success=True)
        except Exception as e:
            return Message(success=False)

    def get_one(self, message):
        return self._get_one_message(message)

    def _get_one_message(self, message):
        return self.collection.find(message, {'_id': 0})

    def get_all(self):
        return self._get_all_message()

    def _get_all_message(self):
        return self.collection.find()

    def get_message_limit(self, count):
        return self._get_message_limit(count)

    def _get_message_limit(self, count):
        return self.collection.find().sort("_id", -1).limit(count)

    def _count_doc(self, doc):
        return self.collection.count_documents(doc)

    def count_doc(self, doc):
        return self._count_doc(doc)


class Producer(ABC):
    def __init__(self, driver: Driver):
        self.driver = driver

    @abstractmethod
    def insert_message(self, message: Dict):
        pass

    @abstractmethod
    def delete_message(self, message: Dict):
        pass

    @abstractmethod
    def update_message(self, message: Dict, new_value: Dict):
        pass

    @abstractmethod
    def get_message(self, message: Dict):
        pass

    @abstractmethod
    def get_all_message(self):
        pass

    @abstractmethod
    def get_message_limit(self, count: int):
        pass

    @abstractmethod
    def get_count_doc(self, doc):
        pass


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)


class MessageProducer(Producer):

    def insert_message(self, message: Dict):
        self.driver.connect()
        result = self.driver.insert(message)
        self.driver.disconnect()
        return result

    def delete_message(self, message: Dict):
        self.driver.connect()
        result = self.driver.delete(message)
        self.driver.disconnect()
        return result

    def update_message(self, message: Dict, new_value: Dict):
        self.driver.connect()
        result = self.driver.update(message, new_value)
        self.driver.disconnect()
        return result

    def get_message(self, message: Dict):
        self.driver.connect()
        result = self.driver.get_one(message)
        self.driver.disconnect()
        return result

    def get_all_message(self):
        self.driver.connect()
        result = self.driver.get_all()
        self.driver.disconnect()
        return result

    def get_message_limit(self, count: int):
        self.driver.connect()
        result = self.driver.get_message_limit(count)
        self.driver.disconnect()
        return result

    def get_count_doc(self, doc):
        self.driver.connect()
        result = self.driver.count_doc(doc)
        self.driver.disconnect()
        return result
