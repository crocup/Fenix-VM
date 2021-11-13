from typing import List
from pydantic import BaseModel


class Status(BaseModel):
    """ """
    success: bool
    message: str


class Create(BaseModel):
    """ ds """
    mask: str
    name: str


class Start(BaseModel):
    name: str


class GetResult(BaseModel):
    status: bool
    data: List
