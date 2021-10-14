from typing import List
from pydantic import BaseModel


class TaskCreate(BaseModel):
    """ ds """
    mask: str
    name: str


class TaskStatus(BaseModel):
    success: bool
    message: str


class TaskStart(BaseModel):
    name: str


class GetTaskResult(BaseModel):
    status: bool
    data: List
