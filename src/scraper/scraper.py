import asyncio
import re
from urllib.parse import urljoin

import httpx
import logging
from typing import List, Optional, Dict

from selectolax.parser import HTMLParser

from src.database.crud import get_car_by_url
from src.scraper.utils import clean_odometer, clean_price, clean_phone_number
from src.config import settings
from src.database.session import async_session

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
        async with async_session() as db:
            while page_num <= settings.PAGES:
                url = f"{self.START_URL}?page={page_num}"
                logger.info(f"Scraping {url}")

                """Try to get list of cars """
                try:
                    cars = await self.get_cars_from_page(url=url)
                    if not cars:
                        logger.info("No more cars. Script STOP.")
                        break

                    for car_url in cars:
                        if await get_car_by_url(db=db, url=car_url):
                            logger.debug(f"Skip duplicate car {car_url}")
                            continue

                    page_num += 1
                    await asyncio.sleep(1)

                except Exception as e:
                    logger.error(f"Error scraping page {page_num}: {str(e)}")
                    break

    async def get_cars_from_page(self, url: str) -> List[str]:
        """Parsing cars from the url"""
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

    async def scrape_car_page(self, url: str):
        """Scrape the data of car from a single page"""
        try:
            resp = await self.client.get(url)
            resp.raise_for_status()
            tree = HTMLParser(resp.text)

            # Base info about car
            title = tree.css_first('h1.head').text().strip() if tree.css_first('h1.head') else None
            price = clean_price(tree.css_first('div.price_value strong').text()) if tree.css_first('div.price_value strong') else None
            odometer = clean_odometer(tree.css_first('div.base-information span.size18').text()) if tree.css_first(
                'div.base-information span.size18') else None

            # Image data
            img_node = tree.css_first('picture img')
            image_url = img_node.attributes.get('src') if img_node else None
            img_count = self._extract_images_count(tree)

            # VIN and number
            vin_code = self._extract_vin(tree)
            car_number = self._extract_car_number(tree)

            # Seller data
            seller_data = await self._extract_seller_data(tree)

            return {
                'url': url,
                'title': title,
                'price_usd': price,
                'odometer': odometer,
                'username': seller_data.get('username'),
                'phone_number': seller_data.get('phone'),
                'image_url': image_url,
                'images_count': img_count,
                'car_number': car_number,
                'car_vin': vin_code
            }

        except Exception as e:
            logger.error(f"Error scraping car page {url}: {str(e)}")
            return None

    async def _extract_seller_data(self, tree) -> Dict:
        seller_data = {"username": None, "phone": None}

        # Seller name
        seller_name_node = tree.css_first('h4.seller_info_name a')
        if seller_name_node:
            seller_data["username"] = seller_name_node.text().strip()

        # Get the seller url
        seller_url = seller_name_node.attributes.get('href') if seller_name_node else None

        if seller_url:
            try:
                resp = await self.client.get(seller_url)
                resp.raise_for_status()

                # Pars phone number
                phone_match = re.search(r'"phone","([^"]+)"', resp.text)
                if phone_match:
                    seller_data['phone'] = clean_phone_number(phone_match.group(1))

                if not seller_data['username']:
                    name_match = re.search(r'"sellerName","([^"]+)"', resp.text)
                    if name_match:
                        seller_data['username'] = name_match.group(1)
            except Exception as e:
                logger.warning(f"Couldn't extract seller info from {seller_url}: {str(e)}")

        return seller_data

    def _extract_images_count(self, tree) -> Optional[int] | None:
        """Extract total images count"""
        count_node = tree.css_first('span.count')
        if count_node:
            text = count_node.text()
            match = re.search(r'из (\d+)', text)
            if match:
                return int(match.group(1))
        return None

    def _extract_vin(self, tree) -> Optional[str] | None:
        """Extract VIN number"""
        vin_node = tree.css_first('span.label-vin')
        if vin_node:
            return vin_node.text().strip()
        return None

    def _extract_car_number(self, tree) -> Optional[str] | None:
        """Extract car number"""
        number_node = tree.css_first('span.state-num')
        if number_node:
            return number_node.text().split()[0]  # Get just the number part
        return None
