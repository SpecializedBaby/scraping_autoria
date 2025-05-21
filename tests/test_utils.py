import pytest
from src.scraper.utils import clean_price, clean_odometer, clean_phone_number


@pytest.mark.parametrize("input_price,expected", [
    ("33 950 $", 33950),
    ("10,000$", 10000),
    ("5 500 €", 5500),
    ("invalid", None),
    (None, None),
])
def test_clean_price(input_price, expected):
    assert clean_price(input_price) == expected


@pytest.mark.parametrize("input_odo,expected", [
    ("95 тыс. км", 95000),
    ("199 тыс", 199000),
    ("50,000 km", 50000),
    ("invalid", None),
    (None, None),
])
def test_clean_odometer(input_odo, expected):
    assert clean_odometer(input_odo) == expected


@pytest.mark.parametrize("input_phone,expected", [
    ("(050) 951 97 40", "+380509519740"),
    ("050 951 97 40", "+380509519740"),
    ("09519740", "+3809519740"),
    ("+380509519740", "+380509519740"),
    ("invalid", None),
    (None, None),
])
def test_clean_phone_number(input_phone, expected):
    assert clean_phone_number(input_phone) == expected
