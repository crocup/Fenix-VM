from pydantic import BaseModel


class Host(BaseModel):
    host: str
