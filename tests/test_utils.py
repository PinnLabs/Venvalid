from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest

from src.venvalid.utils import _cast


@pytest.mark.parametrize(
    "val,expected",
    [
        ("true", True),
        ("True", True),
        ("1", True),
        ("yes", True),
        ("on", True),
        ("false", False),
        ("0", False),
        ("no", False),
        ("off", False),
        ("", False),
        ("maybe", False),  # unexpected value
    ],
)
def test_cast_bool(val, expected):
    assert _cast(val, bool) == expected


def test_cast_list_normal():
    assert _cast("a,b , c", list) == ["a", "b", "c"]


def test_cast_list_empty():
    assert _cast("", list) == [""]


def test_cast_path():
    path = "/tmp/test.txt"
    assert _cast(path, Path) == Path(path)


def test_cast_decimal_valid():
    assert _cast("10.5", Decimal) == Decimal("10.5")


def test_cast_decimal_invalid():
    with pytest.raises(Exception):
        _cast("abc", Decimal)


def test_cast_datetime_valid():
    assert _cast("2024-01-01T10:00:00", datetime) == datetime(2024, 1, 1, 10, 0, 0)


def test_cast_datetime_invalid():
    with pytest.raises(ValueError):
        _cast("not-a-date", datetime)


def test_cast_dict_valid():
    assert _cast('{"debug": true, "port": 8000}', dict) == {"debug": True, "port": 8000}


def test_cast_dict_invalid():
    with pytest.raises(ValueError):
        _cast("{not: valid}", dict)


def test_cast_dict_empty():
    assert _cast("{}", dict) == {}


def test_cast_str():
    assert _cast("hello", str) == "hello"


def test_cast_int_valid():
    assert _cast("42", int) == 42


def test_cast_int_invalid():
    with pytest.raises(ValueError):
        _cast("not-int", int)


def test_cast_float_valid():
    assert _cast("3.14", float) == 3.14


class Dummy:
    pass


def test_cast_unknown_type():
    val = "123"
    dummy_type = Dummy
    with pytest.raises(TypeError):
        _cast(val, dummy_type)
