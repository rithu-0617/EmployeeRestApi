"""
Application configuration for different environments.
"""
import os
from datetime import timedelta


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-me-in-production")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-change-me-in-production")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.environ.get("JWT_ACCESS_TOKEN_HOURS", 1))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(os.environ.get("JWT_REFRESH_TOKEN_DAYS", 30))
    )
    JSON_SORT_KEYS = False

    # Data store path (JSON file; swappable with DB URI later)
    DATA_DIR = os.environ.get(
        "DATA_DIR",
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "data"),
    )


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    DATA_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "data", "test"
    )


class ProductionConfig(BaseConfig):
    """Production configuration."""
    DEBUG = False
    TESTING = False


config_by_name: dict[str, type] = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
