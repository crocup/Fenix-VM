from pydantic import BaseModel


class Message(BaseModel):
    success: bool

