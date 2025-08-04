from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest

from src.venvalid import (
    bool_,
    datetime_,
    decimal_,
    int_,
    json_,
    list_,
    path_,
    str_,
    venvalid,
)


def test_int_helper_structure():
    helper = int_(default=5, allowed=[5, 10], validate=lambda x: x > 0)
    assert helper[0] is int
    assert helper[1]["default"] == 5
    assert helper[1]["allowed"] == [5, 10]
    assert callable(helper[1]["validate"])


def test_str_helper_structure():
    helper = str_(default="dev", allowed=["dev", "prod"])
    assert helper[0] is str
    assert helper[1]["default"] == "dev"
    assert helper[1]["allowed"] == ["dev", "prod"]


def test_bool_helper_structure():
    assert bool_(default=True) == (bool, {"default": True})


def test_list_helper_structure():
    assert list_(default=["a", "b"]) == (list, {"default": ["a", "b"]})


def test_path_helper_structure():
    p = Path("/tmp")
    assert path_(default=p) == (Path, {"default": p})


def test_decimal_helper_structure():
    d = Decimal("9.9")
    assert decimal_(default=d) == (Decimal, {"default": d})


def test_datetime_helper_structure():
    dt = datetime(2025, 1, 1)
    assert datetime_(default=dt) == (datetime, {"default": dt})


def test_json_helper_structure():
    j = {"key": "value"}
    assert json_(default=j) == (dict, {"default": j})


def test_int_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("PORT", "8080")
    config = venvalid({"PORT": int_(default=8000)})
    assert config["PORT"] == 8080


def test_bool_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("DEBUG", "yes")
    config = venvalid({"DEBUG": bool_(default=False)})
    assert config["DEBUG"] is True


def test_path_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("LOG_PATH", "/var/log.txt")
    config = venvalid({"LOG_PATH": path_()})
    assert config["LOG_PATH"] == Path("/var/log.txt")


def test_decimal_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("TAX", "19.75")
    config = venvalid({"TAX": decimal_()})
    assert config["TAX"] == Decimal("19.75")


def test_datetime_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("START_TIME", "2025-01-01T00:00:00")
    config = venvalid({"START_TIME": datetime_()})
    assert config["START_TIME"] == datetime(2025, 1, 1)


def test_json_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("SETTINGS", '{"mode": "dark"}')
    config = venvalid({"SETTINGS": json_()})
    assert config["SETTINGS"] == {"mode": "dark"}


def test_list_helper_used_in_env(monkeypatch):
    monkeypatch.setenv("HOSTS", "a.com,b.com , c.com")
    config = venvalid({"HOSTS": list_()})
    assert config["HOSTS"] == ["a.com", "b.com", "c.com"]


def test_int_helper_invalid_value(monkeypatch):
    monkeypatch.setenv("PORT", "not-a-number")
    with pytest.raises(SystemExit):
        venvalid({"PORT": int_()})


def test_json_helper_invalid(monkeypatch):
    monkeypatch.setenv("SETTINGS", "{invalid json}")
    with pytest.raises(SystemExit):
        venvalid({"SETTINGS": json_()})


def test_custom_validation_fails(monkeypatch):
    monkeypatch.setenv("PORT", "80")
    with pytest.raises(SystemExit):
        venvalid({"PORT": int_(validate=lambda x: x >= 1024)})
