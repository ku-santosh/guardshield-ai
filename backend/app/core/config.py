import os
from typing import Any, Dict, List, Optional, Union
from pydantic import Field
from pydantic_settings import SettingsConfigDict, Basesettings


class Settings(Basesettings):
    """Application settings."""

    PROJECT_NAME: str = "GuardShield AI Enterprise Platform"
    API_V1_STR: str = "/api/v1"
    ENVIRONMENT: str = Field(default="development", validation_alias="ENV")
    
    # Database Layer Abstraction Configuration
    USE_DATABASE: bool = Field(default=False)
    DATABASE_URL: Optional[str] = Field(default=None)
    REDIS_URL: str = Field(default="redis://localhost:6379/0")
    
    # Security Configuration
    JWT_SECRET_KEY: str = Field(default="SYSTEM_SUPER_SECRET_KEY_PROD_CHANGE_ME")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # LLM Stack & Observability Backbones
    OPENAI_API_KEY: str = Field(default="sk-placeholder")
    LANGFUSE_PUBLIC_KEY: Optional[str] = None
    LANGFUSE_SECRET_KEY: Optional[str] = None
    LANGFUSE_HOST: str = "https://cloud.langfuse.com"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

settings = Settings()