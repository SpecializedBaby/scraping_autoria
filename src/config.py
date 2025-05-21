from pydantic import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "db"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_NAME: str = "auto_ria"

    # Scraper settings
    SCRAPE_TIME: str = "12:00"  # HH:MM format
    DUMP_TIME: str = "12:30"  # HH:MM format

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/auto_ria_scraper.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

settings = Settings()
