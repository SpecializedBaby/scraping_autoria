from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from src.scraper.scraper import AutoRiaScraper
from dumper import dump_database
import httpx
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class AutoRiaScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.scrape_time = "12:00"  # Default from config
        self.dump_time = "12:30"  # Default from config

    async def run_scraper(self):
        """Execute the scraping task"""
        logger.info("Starting scheduled scraping task")
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                scraper = AutoRiaScraper(client)
                await scraper.scrape()
        except Exception as e:
            logger.error(f"Scraping failed: {str(e)}")
        logger.info("Finished scraping task")

    async def run_dump(self):
        """Execute the database dump task"""
        logger.info("Starting scheduled database dump")
        try:
            await dump_database()
        except Exception as e:
            logger.error(f"Database dump failed: {str(e)}")
        logger.info("Finished database dump")

    def start(self):
        """Start the scheduled tasks"""
        # Schedule scraping
        hour, minute = map(int, self.scrape_time.split(':'))
        self.scheduler.add_job(
            self.run_scraper,
            trigger=CronTrigger(hour=hour, minute=minute),
            name="daily_auto_ria_scrape"
        )

        # Schedule dumping
        dump_hour, dump_minute = map(int, self.dump_time.split(':'))
        self.scheduler.add_job(
            self.run_dump,
            trigger=CronTrigger(hour=dump_hour, minute=dump_minute),
            name="daily_db_dump"
        )

        self.scheduler.start()
        logger.info(f"Scheduler started. Scraping at {self.scrape_time}, dumps at {self.dump_time}")
