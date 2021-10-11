from pydantic import BaseModel


class HostIn(BaseModel):
    """  """
    host: str
    options: str


class HostOut(BaseModel):
    """  """
    status: bool
    job: str
