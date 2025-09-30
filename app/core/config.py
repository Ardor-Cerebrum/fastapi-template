"""
Core configuration settings for the FastAPI application.

This module handles all environment-based configuration using Pydantic BaseSettings.
"""

from typing import List, Union

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    PROJECT_NAME: str = "FastAPI Template"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A simple FastAPI template"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    ALLOW_ORIGINS: List[str] = ["*"]
    ALLOW_CREDENTIALS: bool = True
    ALLOW_METHODS: List[str] = ["*"]
    ALLOW_HEADERS: List[str] = ["*"]
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings instance."""
    return settings


# Environment-specific configurations
def is_development() -> bool:
    """Check if running in development environment."""
    return settings.ENVIRONMENT.lower() in ("development", "dev", "local")


def is_production() -> bool:
    """Check if running in production environment."""
    return settings.ENVIRONMENT.lower() in ("production", "prod")
