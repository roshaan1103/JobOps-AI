from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "JobOps AI"
    app_env: str = "development"
    log_level: str = "INFO"

    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    database_url: str

    ollama_base_url: str = "http://host.docker.internal:11434"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()