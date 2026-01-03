from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    database_url: str
    at_minutes: int
    rt_days: int
    secret_key: str
    algorithm: str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


@lru_cache()
def get_setting() -> Settings:
    s = Settings()
    return s