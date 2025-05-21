import re


def clean_price(price: str) -> int|None:
    if not price:
        return None
    try:
        return int(re.sub(r'[^\d]', '', price))
    except (ValueError, TypeError):
        return None


def clean_odometer(odometer: str) -> int|None:
    if not odometer:
        return None
    try:
        if "тыс" in odometer:
            return int(float(odometer.replace('тыс', '').strip())) * 1000
        return int(re.sub(r'[^\d]', '', odometer))
    except (ValueError, TypeError):
        return None


def clean_phone_number(phone):
    if not phone:
        return None
        # Remove all non-digit characters
    digits = re.sub(r'[^\d]', '', phone)
    # Add +380 if it's a Ukrainian number without country code
    if len(digits) == 9 and digits.startswith('0'):
        return f"+380{digits[1:]}"
    elif len(digits) == 10 and digits.startswith('0'):
        return f"+38{digits}"
    elif len(digits) == 12 and digits.startswith('380'):
        return f"+{digits}"
    return digits
