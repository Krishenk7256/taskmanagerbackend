from enum import Enum
from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    development = "development"
    staging = "staging"
    production = "production"


class Settings(BaseSettings):
    ENV: Environment = Environment.development
    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SQL_ECHO: bool = False
    # В development можно включить автосоздание таблиц; в production — только Alembic
    AUTO_CREATE_TABLES: bool = True

    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10

    CORS_ORIGINS: list[str] = Field(default_factory=lambda: ["*"])

    SECRET_KEY: str = Field(default="your-secret-key-change-in-production", min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def split_cors_origins(cls, v: object) -> object:
        if isinstance(v, str) and not v.startswith("["):
            return [s.strip() for s in v.split(",") if s.strip()]
        return v

    @field_validator("SQL_ECHO", mode="before")
    @classmethod
    def sql_echo_from_env(cls, v: object) -> object:
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes")
        return v

    @field_validator("AUTO_CREATE_TABLES", mode="before")
    @classmethod
    def auto_create_tables_from_env(cls, v: object) -> object:
        if isinstance(v, str):
            return v.lower() in ("1", "true", "yes")
        return v

    @model_validator(mode="after")
    def production_safety(self) -> "Settings":
        if self.ENV == Environment.production:
            if self.SECRET_KEY.startswith("change-me") or len(self.SECRET_KEY) < 32:
                raise ValueError(
                    "Production requires SECRET_KEY of at least 32 characters "
                    "and not the default placeholder"
                )
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()


# Совместимость: импорт `from app.core.config import settings`
settings = get_settings()
