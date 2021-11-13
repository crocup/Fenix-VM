from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

API_PREFIX = "/api/v1"
VERSION = "0.0.20"
config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=True)
PROJECT_NAME: str = config("PROJECT_NAME", default="FSEC VM")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
DATABASE_IP: str = config("DATABASE_IP", default="127.0.0.1")
DATABASE_PORT: int = config("DATABASE_PORT", default=27017)
# https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/app/api/routes/tags.py
