import pytest
from unittest.mock import AsyncMock, patch
from src.scraper.scraper import AutoRiaScraper
from httpx import Response


@pytest.fixture
def mock_client():
    return AsyncMock()


@pytest.mark.asyncio
async def test_get_cars_from_page(mock_client):
    # Mock HTML response
    html_content = """
    <html>
        <body>
            <section class="ticket-item">
                <div class="hide" data-link-to-view="/auto_test1.html"></div>
            </section>
            <section class="ticket-item">
                <div class="hide" data-link-to-view="/auto_test2.html"></div>
            </section>
        </body>
    </html>
    """
    mock_client.get.return_value = Response(200, content=html_content)

    scraper = AutoRiaScraper(mock_client)
    listings = await scraper.get_cars_from_page("https://auto.ria.com/test")

    assert len(listings) == 2
    assert "auto_test1.html" in listings[0]
    assert "auto_test2.html" in listings[1]


@pytest.mark.asyncio
async def test_scrape_car_page(mock_client):
    # Mock car page HTML
    car_html = """
    <html>
        <head>
            <title>Test Car</title>
        </head>
        <body>
            <h1 class="head">Test Car 2020</h1>
            <div class="price_value"><strong>10 000 $</strong></div>
            <div class="base-information"><span class="size18">50</span> тыс. км</div>
            <picture>
                <img src="https://test.com/image.jpg">
            </picture>
            <span class="count">из 10</span>
            <span class="label-vin">VIN123456789</span>
            <h4 class="seller_info_name">
                <a href="https://auto.ria.com/seller/123">Test Seller</a>
            </h4>
        </body>
    </html>
    """

    # Mock seller page HTML
    seller_html = """
    <html>
        <script>
            window.__STATE__ = {"data":[["phone","(050) 123 45 67"],["sellerName","Test Seller"]]}
        </script>
    </html>
    """

    # Configure mock client responses
    mock_client.get.side_effect = [
        Response(200, content=car_html),
        Response(200, content=seller_html),
    ]

    scraper = AutoRiaScraper(mock_client)
    car_data = await scraper.scrape_car_page("https://auto.ria.com/test_car.html")

    assert car_data is not None
    assert car_data["title"] == "Test Car 2020"
    assert car_data["price_usd"] == 10000
    assert car_data["odometer"] == 50000
    assert car_data["image_url"] == "https://test.com/image.jpg"
    assert car_data["images_count"] == 10
    assert car_data["car_vin"] == "VIN123456789"
    assert car_data["username"] == "Test Seller"
    assert car_data["phone_number"] == "+380501234567"


@pytest.mark.asyncio
async def test_scrape_car_page_error(mock_client):
    mock_client.get.return_value = Response(404)

    scraper = AutoRiaScraper(mock_client)
    car_data = await scraper.scrape_car_page("https://auto.ria.com/invalid")

    assert car_data is None
