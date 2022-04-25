from pydantic import BaseModel


class Message(BaseModel):
    success: bool


class Host(BaseModel):
    host: str


class Result(BaseModel):
    success: bool


class DiscoveryMessage(BaseModel):
    service: str
    host: str
    mac_addr: str
    time: str
