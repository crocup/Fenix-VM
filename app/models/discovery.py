from typing import List
from pydantic import BaseModel


class Create(BaseModel):
    mask: str
    name: str


class Host(BaseModel):
    host: str


class Edit(BaseModel):
    host: str
    name: str


class ResultTask(BaseModel):
    status: bool
    data: List


class Result(BaseModel):
    success: bool
