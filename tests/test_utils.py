from datetime import date

from dapodix.utils import parse_range
from dapodix.utils import snake_to_title
from dapodix.utils import parse_date


def test_parse_range():
    value = "1-10,15,98-100"
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 98, 99, 100]
    result = parse_range(value)
    assert result == expected


def test_snake_to_title():
    value = "pESErtA_DidiK"
    expected = "Peserta Didik"
    result = snake_to_title(value)
    assert result == expected


def test_parse_date():
    value = "1/12/2001"
    expected = date(2001, 12, 1)
    result = parse_date(value)
    assert result == expected
