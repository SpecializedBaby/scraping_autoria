import asyncio
import logging
from src.scraper.scraper import AutoRiaScraper
from src.database.session import get_db
import httpx


# Настройка логгирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)


async def main():
    async with httpx.AsyncClient(timeout=30.0) as client:
        scraper = AutoRiaScraper(client)
        await scraper.scrape()

if __name__ == "__main__":
    asyncio.run(main())
