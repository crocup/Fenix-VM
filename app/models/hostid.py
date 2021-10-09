from typing import List
from pydantic import BaseModel


class HostIn(BaseModel):
    """  """
    host: str
    options: str


class HostOut(BaseModel):
    """  """
    status: bool
    job: str


class Discovery(BaseModel):
    """ ds """
    status: bool
    data: List


class Task(BaseModel):
    """ """
    success: bool
