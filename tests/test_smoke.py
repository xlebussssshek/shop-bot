from src.utils.validators import is_valid_phone


def test_phone_validator_ok():
    assert is_valid_phone('+7 (999) 123-45-67')


def test_phone_validator_fail():
    assert not is_valid_phone('abc123')
