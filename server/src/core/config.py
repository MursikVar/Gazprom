from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
import secrets
import os

DOTENV = os.path.join(os.path.dirname(__file__), "../../.env")

class Config(BaseSettings):

    DATABASE_URL: PostgresDsn

    JWT_ALG: str
    JWT_SECRET: str = secrets.token_urlsafe(32)
    JWT_EXP: int

    EMAIL_RESET_CODE_EXP:int

    REDIS_HOST: str
    REDIS_PORT: int

    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = True

    model_config = SettingsConfigDict(env_file=DOTENV)

settings = Config()