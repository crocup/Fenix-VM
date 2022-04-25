from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Discovery API"
    APP_VERSION: str = "0.1.1"
    DEBUG: bool = True
    CORE_IP: str = "localhost"
    RABBITMQ: str = "localhost"
    RABBITMQ_QUEUE: str = "fsec"
    RABBITMQ_KEY: str = "fsec"


settings = Settings()
