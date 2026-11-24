from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Определяем корневую папку проекта
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()