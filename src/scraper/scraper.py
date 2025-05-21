import asyncio
from urllib.parse import urljoin

import httpx
import logging
from typing import List

from selectolax.parser import HTMLParser

logger = logging.getLogger(__name__)


class AutoRiaScraper:
    BASE_URL = "https://auto.ria.com"
    START_URL = "https://auto.ria.com/car/used/"

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def scrape(self):
        """Start scraping from START_URL with pagination"""
        """https://auto.ria.com/car/used/?page=1"""
        page_num = 1
        while True:
            url = f"{self.START_URL}?page={page_num}"
            logger.info(f"Scraping {url}")

            """Try to get list of cars """



    async def get_list_items(self, url: str) -> List[str]:
        """Parsing cars from this url"""
        try:
            resp = await self.client.get(url)
            resp.raise_for_status()

            tree = HTMLParser(resp.text)
            cars = []

            for node in tree.css('section.ticket-item'):
                link = node.css_first('div[data-link-to-view]')
                if link:
                    path = link.attributes.get('data-link-to-view')
                    if path:
                        cars.append(urljoin(self.BASE_URL, path))

            return cars

        except Exception as e:
            logger.error(f"Error getting list of car from {url}: {str(e)}")
            return []
