from typing import List
from pydantic import BaseModel


class TaskResult(BaseModel):
    """ ds """
    status: bool
    data: List


class Task(BaseModel):
    """ """
    success: bool
