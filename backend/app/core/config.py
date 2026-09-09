import os

try:
    from pydantic_settings import BaseSettings
    class Settings(BaseSettings):
        PROJECT_NAME: str = "200-Day ML Systems Execution Dashboard"
        API_V1_STR: str = "/api/v1"
        SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-200-day-ml-dashboard")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ml_dashboard.db")
        TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")
        class Config:
            case_sensitive = True
    settings = Settings()
except ImportError:
    class Settings:
        PROJECT_NAME: str = "200-Day ML Systems Execution Dashboard"
        API_V1_STR: str = "/api/v1"
        SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key-change-in-production-200-day-ml-dashboard")
        ALGORITHM: str = "HS256"
        ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
        DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ml_dashboard.db")
        TIMEZONE: str = os.getenv("TIMEZONE", "Asia/Kolkata")
    settings = Settings()
