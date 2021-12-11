from pydantic import BaseSettings
from app.core.config import VERSION, PROJECT_NAME


class Settings(BaseSettings):
    APP_NAME: str = PROJECT_NAME
    APP_VERSION: str = VERSION
    ADMIN_MAIL: str = "patunutap@gmail.com"
    MASK: str = "192.168.1.0/24"
