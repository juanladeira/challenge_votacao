from zoneinfo import ZoneInfo

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

TIMEZONE = ZoneInfo("America/Sao_Paulo")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Project
    PROJECT_NAME: str = "challenge_votacao"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://challenge_votacao:challenge_votacao@localhost:5432/challenge_votacao",
    )

    # JWT
    SECRET_KEY: str = Field(default="insecure-dev-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Admin padrão (seed global)
    ADMIN_DEFAULT_USERNAME: str = "admin"
    ADMIN_DEFAULT_PASSWORD: str = "admin"

    # Criptografia de campos sensíveis (Fernet)
    ENCRYPTION_KEY: str = Field(default="")

    # Redis (Celery broker + rate limit)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")

    # E-mail (Mailpit em dev, SMTP real em prod)
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 1026
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@challenge_votacao.com.br"

    # Storage S3 / MinIO
    S3_ENDPOINT_URL: str = "http://localhost:9020"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin"
    S3_BUCKET: str = "challenge_votacao"
    S3_REGION: str = "us-east-1"

    # Trial padrão (dias)
    DEFAULT_TRIAL_DAYS: int = 30

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"


settings = Settings()
