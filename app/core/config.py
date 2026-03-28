from pydantic import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost/dbname"

    class Config:
        env_file = ".env"

setting = Settings()