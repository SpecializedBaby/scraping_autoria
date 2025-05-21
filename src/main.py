import asyncio
import logging
from src.scraper.scraper import AutoRiaScraper
from src.database.session import engine, async_session
from src.database.models import Base
import httpx
from alembic.config import Config
from alembic import command


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def check_and_apply_migrations():
    try:
        logger.info("run Migrations")
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Migrated success")
    except Exception as e:
        logger.error(f"Error Migrations: {str(e)}")
        raise


async def init_db():
    """initializing DB"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def run_scraper():
    """Runner"""
    async with httpx.AsyncClient(timeout=30.0) as client:
        scraper = AutoRiaScraper(client)
        await scraper.scrape()


async def main():
    try:
        await check_and_apply_migrations()
        await init_db()

        logger.info("Scraper AutoRia starting...")
        await run_scraper()

    except Exception as e:
        logger.error(f"Erorr in main: {str(e)}")
    finally:
        logger.info("Scripts ended correct!")


if __name__ == "__main__":
    asyncio.run(main())
