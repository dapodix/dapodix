from dapodix.utils import parse_range


def test_parse_range():
    value = "1-10,15"
    expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]
    result = parse_range(value)
    assert result == expected
