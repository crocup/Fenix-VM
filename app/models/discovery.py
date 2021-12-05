from typing import List
from pydantic import BaseModel


class Create(BaseModel):
    mask: str
    name: str


class Start(BaseModel):
    uuid: str


class Edit(BaseModel):
    uuid: str
    mask: str
    name: str


class ResultTask(BaseModel):
    status: bool
    data: List


class Result(BaseModel):
    success: bool
