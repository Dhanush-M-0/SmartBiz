import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class"""
    # Environment
    ENV = os.getenv("FLASK_ENV", "production")

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    # Flask
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")
    DEBUG = False
    TESTING = False

    # Email
    EMAIL_SENDER = os.getenv("EMAIL_SENDER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

    # Reports
    REPORTS_OUTPUT_DIR = os.getenv("REPORTS_OUTPUT_DIR", "reports_output")

    # Security
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    """Development configuration"""
    ENV = "development"
    DEBUG = True
    TESTING = False
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False


class ProductionConfig(Config):
    """Production configuration"""
    ENV = "production"
    DEBUG = False
    TESTING = False
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration"""
    ENV = "testing"
    DEBUG = True
    TESTING = True
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False


def get_config():
    """Get configuration object based on FLASK_ENV"""
    env = os.getenv("FLASK_ENV", "production").lower()

    if env == "development":
        return DevelopmentConfig
    elif env == "testing":
        return TestingConfig
    else:
        return ProductionConfig
