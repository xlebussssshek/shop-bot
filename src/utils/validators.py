import re


PHONE_PATTERN = re.compile(r'^\+?[0-9\-\s()]{10,20}$')


def is_valid_phone(phone: str) -> bool:
    return bool(PHONE_PATTERN.match(phone.strip()))
