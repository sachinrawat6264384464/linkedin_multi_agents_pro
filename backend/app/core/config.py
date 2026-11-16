from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Application Basics
    APP_NAME: str = "LinkedIn AgentOS"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = Field(default="dev-super-secret-key-32chars-min-change-prod")
    JWT_SECRET_KEY: str = Field(default="jwt-super-secret-key-32chars-min-change-prod")
    APP_ENCRYPTION_KEY: str = Field(default="dGhpcy1pcy1hLXNhbXBsZS0zMmJ5dGUtZW5jcnlwdGlvbi1rZXk=")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    # Server Binding
    HOST: str = "0.0.0.0"
    PORT: int = Field(default_factory=lambda: int(os.environ.get("PORT", 8000)))
    FRONTEND_URL: str = "http://localhost:3000"
    BACKEND_URL: str = "http://localhost:8000"
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000"
    ]

    # Database (Neon PostgreSQL)
    DATABASE_URL: str = "postgresql+asyncpg://neondb_owner:npg_placeholder@ep-sample-pooler.us-east-2.aws.neon.tech/neondb?ssl=require"
    DATABASE_URL_DIRECT: Optional[str] = "postgresql+psycopg2://neondb_owner:npg_placeholder@ep-sample.us-east-2.aws.neon.tech/neondb?sslmode=require"
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    # Cloudinary Storage
    CLOUDINARY_CLOUD_NAME: str = ""
    CLOUDINARY_API_KEY: str = ""
    CLOUDINARY_API_SECRET: str = ""

    # Ollama Local LLM Execution
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:7b-instruct"
    OLLAMA_TIMEOUT: int = 120

    # LinkedIn OAuth 2.0
    LINKEDIN_CLIENT_ID: str = ""
    LINKEDIN_CLIENT_SECRET: str = ""
    LINKEDIN_REDIRECT_URI: str = "http://localhost:8000/api/v1/publishing/oauth/callback"

    # Web Search
    SEARCH_PROVIDER: str = "mock"  # "mock" or "tavily"
    TAVILY_API_KEY: str = ""

    # Langfuse Telemetry (Optional)
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() == "production"

    @property
    def is_database_configured(self) -> bool:
        return bool(self.DATABASE_URL and "npg_placeholder" not in self.DATABASE_URL)

    @property
    def is_cloudinary_configured(self) -> bool:
        return bool(
            self.CLOUDINARY_CLOUD_NAME
            and self.CLOUDINARY_API_KEY
            and self.CLOUDINARY_API_SECRET
            and "placeholder" not in self.CLOUDINARY_CLOUD_NAME.lower()
            and "placeholder" not in self.CLOUDINARY_API_KEY.lower()
        )

    @property
    def is_linkedin_configured(self) -> bool:
        return bool(
            self.LINKEDIN_CLIENT_ID
            and self.LINKEDIN_CLIENT_SECRET
            and "placeholder" not in self.LINKEDIN_CLIENT_ID.lower()
            and "placeholder" not in self.LINKEDIN_CLIENT_SECRET.lower()
        )


settings = Settings()
