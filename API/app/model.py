from pydantic import BaseModel


class Host(BaseModel):
    host: str


class Result(BaseModel):
    success: bool
