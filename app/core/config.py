from typing import List
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret


API_PREFIX = "/api/v1"
VERSION = "0.0.12"
config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=True)
PROJECT_NAME: str = config("PROJECT_NAME", default="FSEC VM")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)
