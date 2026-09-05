from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="MODELLEDGER_")

    environment: str = "development"
    database_url: str = "sqlite:///./modelledger.db"
    jwt_secret: str = Field(default="local-development-secret-change-before-production", min_length=32)
    jwt_issuer: str = "modelledger"
    jwt_audience: str = "modelledger-api"
    access_token_minutes: int = 60
    artifact_bucket: str = "model-artifacts"
    minio_endpoint_url: str = "http://127.0.0.1:9000"
    celery_broker_url: str = "redis://127.0.0.1:6379/0"
    celery_result_backend: str = "redis://127.0.0.1:6379/1"
    mlflow_tracking_uri: str = "http://127.0.0.1:5000"
    cors_origins: list[str] = ["http://127.0.0.1:5173", "http://localhost:5173"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
