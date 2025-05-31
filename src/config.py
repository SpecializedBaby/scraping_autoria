from pydantic_settings import BaseSettings
from pathlib import Path
import os


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    DATABASE_URL: str

    # Scraper settings
    SCRAPE_TIME: str
    DUMP_TIME: str

    # Logging
    LOG_LEVEL: str
    LOG_FILE: str

    # Scraping
    PAGES: int | bool

    class Config:
        env_file = ".env.dev"
        env_file_encoding = "utf-8"
        extra = "forbid"


# Create logs directory if it doesn't exist
Path("logs").mkdir(exist_ok=True)

settings = Settings()
