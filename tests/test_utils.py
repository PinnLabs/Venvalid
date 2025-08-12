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
        ("False", False),
        ("0", False),
        ("no", False),
        ("off", False),
    ],
)
def test_cast_bool_valid(val, expected):
    assert _cast(val, bool) == expected


@pytest.mark.parametrize("val", ["", "maybe", "truth", "none"])
def test_cast_bool_invalid(val):
    with pytest.raises(ValueError):
        _cast(val, bool)


def test_cast_list_normal():
    assert _cast("a,b , c", list) == ["a", "b", "c"]


def test_cast_list_empty():
    assert _cast("", list) == []


def test_cast_path():
    path = "/tmp/test.txt"
    assert _cast(path, Path) == Path(path)


def test_cast_decimal_valid():
    assert _cast("10.5", Decimal) == Decimal("10.5")


def test_cast_decimal_invalid():
    with pytest.raises(ValueError):
        _cast("abc", Decimal)


def test_cast_datetime_valid_iso():
    assert _cast("2024-01-01T10:00:00", datetime) == datetime(2024, 1, 1, 10, 0, 0)


def test_cast_datetime_valid_custom_format():
    val = "01-02-2025 15:30"
    fmt = "%d-%m-%Y %H:%M"
    assert _cast(val, datetime, datetime_format=fmt) == datetime(2025, 2, 1, 15, 30)


def test_cast_datetime_invalid():
    with pytest.raises(ValueError):
        _cast("not-a-date", datetime)


def test_cast_dict_valid():
    assert _cast('{"debug": true, "port": 8000}', dict) == {"debug": True, "port": 8000}


def test_cast_list_json_valid():
    assert _cast('["a", "b", "c"]', list) == ["a", "b", "c"]


def test_cast_dict_invalid_json():
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
    def __init__(self, v):
        raise TypeError("Cannot instantiate Dummy with value")


def test_cast_unknown_type():
    val = "123"
    with pytest.raises(ValueError):
        _cast(val, Dummy)
