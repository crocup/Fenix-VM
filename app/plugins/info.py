"""
info.html
Dmitry Livanov, 2021
"""
from __future__ import annotations
import requests
from app.config import DATABASE
from app.service.database.database import Storage
from abc import ABC, abstractmethod, abstractproperty
from typing import Any


def delete_task(uuid: str):
    """
    Удаление информации о задаче
    uuid: UUID номер задачи
    """
    try:
        requests.post(f"{DATABASE}/delete", json={"data": {"uuid": uuid},
                                                  "base": "scanner", "collection": "result"})
    except Exception as e:
        print(e)


def create_report():
    pass


def vulnerability_info(vulnerability: str):
    """

    """
    try:
        cve_upper = str(vulnerability).upper()
        knowledge_base = Storage(db='vulndb', collection='cve')
        data = knowledge_base.data_one(data={"cve": cve_upper})
        return data
    except Exception as e:
        print(e)
