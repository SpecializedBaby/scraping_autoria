import asyncio
import logging
from alembic.config import Config
from alembic import command

from src.database.session import engine
from src.database.models import Base
from src.scheduler import AutoRiaScheduler
from src.config import settings


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def run_migrations():
    """Run database migrations"""
    try:
        alembic_cfg = Config("alembic.ini")
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations applied successfully")
    except Exception as e:
        logger.error(f"Migration failed: {str(e)}")
        raise


async def main():
    """Main application entry point"""
    try:
        logger.info("Starting AutoRia Scraper Service 2.0")

        # 2. Initialize database (extra safety)
        await init_db()

        # 3. Start scheduler
        scheduler = AutoRiaScheduler()
        scheduler.scrape_time = settings.SCRAPE_TIME
        scheduler.dump_time = settings.DUMP_TIME
        scheduler.start()

        # Keep application running
        while True:
            await asyncio.sleep(1)

    except Exception as e:
        logger.error(f"Application error: {str(e)}")
    finally:
        logger.info("Service stopped")


if __name__ == "__main__":
    asyncio.run(main())
