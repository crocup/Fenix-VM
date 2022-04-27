# Config will be read from environment variables and/or ".env" files.
from starlette.config import Config

config = Config(".env")
DEBUG = config('DEBUG', cast=bool, default=False)
APP_NAME = config('APP_NAME', cast=str, default="FSEC API")
APP_VERSION = config('APP_VERSION', cast=str, default="0.1.1")
rabbit_mq = config('rabbit_mq', cast=str, default="localhost")