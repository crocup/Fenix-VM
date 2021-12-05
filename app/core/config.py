import datetime
from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from pathlib import Path


API_PREFIX = "/api/v1"
VERSION = "0.0.21"
config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=True)
PROJECT_NAME: str = config("PROJECT_NAME", default="FSEC VM")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
# database
DATABASE_IP: str = config("DATABASE_IP", default="0.0.0.0")
DATABASE_PORT: int = config("DATABASE_PORT", default=27017)
# year feeds
NOW_YEAR: int = config("NOW_YEAR", default=datetime.datetime.now().year)
START_YEAR: int = config("START_YEAR", default=2002)

DIR_FEEDS: str = ""

# https://github.com/nsidnev/fastapi-realworld-example-app/blob/master/app/api/routes/tags.py