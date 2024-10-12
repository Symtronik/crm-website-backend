from functools import lru_cache
import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Security
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    HASHING_ALGORITHM: str = os.environ.get("HASHING_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    # DB Settings
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # User
    ADMIN_USERNAME: str = os.environ.get("ADMIN_USERNAME")
    ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD")
    ADMIN_EMAIL: str = os.environ.get("ADMIN_EMAIL")


    class Config:

        env_file = ".env"


@lru_cache
def get_settings():
    settings = Settings()
    # Debugowanie
    print(f"SECRET_KEY: {settings.SECRET_KEY}")
    print(f"DATABASE_URL: {settings.DATABASE_URL}")
    return settings