from pydantic import BaseSettings
from app.core.config import VERSION, PROJECT_NAME


class Settings(BaseSettings):
    app_name: str = PROJECT_NAME
    app_version: str = VERSION
    admin_email: str = "patunutap@gmail.com"
