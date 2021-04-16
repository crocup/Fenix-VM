"""
info.html
Dmitry Livanov, 2021
"""
from __future__ import annotations
from app.service.database import MessageProducer, MongoDriver


def delete_task(uuid: str):
    """
    Удаление информации о задаче
    uuid: UUID номер задачи
    """
    try:
        message_mongo = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                    base="scanner", collection="result"))
        message_mongo.delete_message({"uuid": uuid})
    except Exception as e:
        print(e)


def create_report():
    pass


def vulnerability_info(vulnerability: str):
    """

    """
    try:
        cve_upper = str(vulnerability).upper()
        message_mongo = MessageProducer(MongoDriver(host='localhost', port=27017,
                                                    base="vulndb", collection="cve"))
        data = message_mongo.get_message({"cve": cve_upper})
        return data
    except Exception as e:
        print(e)
