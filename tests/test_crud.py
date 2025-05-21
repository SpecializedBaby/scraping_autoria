import pytest

from src.database.crud import create_car, get_car_by_url


@pytest.mark.asyncio
async def test_create_and_get_car(db_session):
    car_data = {
        "url": "https://auto.ria.com/test_car.html",
        "title": "Test Car",
        "price_usd": 10000,
    }

    created_car = await create_car(db_session, car_data)
    assert created_car is not None
    assert created_car.url == car_data['url']

    # Get car by url
    car = await get_car_by_url(db_session, car_data['url'])
    assert car is not None
    assert car.url == car_data['url']
    assert car.title == car_data['title']
    assert car.price_usd == car_data['price_usd']


@pytest.mark.asyncio
async def test_get_non_existent_car(db_session):
    car = await get_car_by_url(db_session, "")
    assert car is None
