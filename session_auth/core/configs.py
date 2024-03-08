from typing import Any
from pydantic_settings import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    DB_URL: str = "postgresql+asyncpg://margarida:1234@localhost:5432/postgres"
    DBBaseModel: Any = declarative_base()

    JWT_SECRET: str = 'kn2yxVHTgjXMZwpV0V8_hJ2SaVVQ2aU4UC5ZYeDGhY4'
    """
    import secrets
    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTE: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings = Settings()

