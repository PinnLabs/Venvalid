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


def test_basic_types(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("SECRET", "abc123")

    config = venvalid({"DEBUG": bool, "PORT": int, "SECRET": str})

    assert config["DEBUG"] is True
    assert config["PORT"] == 8000
    assert config["SECRET"] == "abc123"


def test_list_type(monkeypatch):
    monkeypatch.setenv("HOSTS", "a.com, b.com ,c.com")
    config = venvalid({"HOSTS": list})
    assert config["HOSTS"] == ["a.com", "b.com", "c.com"]


def test_enum_values(monkeypatch):
    monkeypatch.setenv("MODE", "prod")
    config = venvalid({"MODE": ["dev", "prod", "test"]})
    assert config["MODE"] == "prod"


def test_allowed_values(monkeypatch):
    monkeypatch.setenv("REGION", "us")
    config = venvalid({"REGION": (str, {"allowed": ["us", "eu"]})})
    assert config["REGION"] == "us"


def test_default_value(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)
    config = venvalid({"ENV": (str, {"default": "dev"})})
    assert config["ENV"] == "dev"


def test_validate_function(monkeypatch):
    monkeypatch.setenv("PORT", "8080")
    config = venvalid({"PORT": (int, {"validate": lambda x: 1024 <= x <= 65535})})
    assert config["PORT"] == 8080


def test_missing_required(monkeypatch):
    monkeypatch.delenv("MISSING", raising=False)
    with pytest.raises(SystemExit):
        venvalid({"MISSING": str})


def test_enum_invalid(monkeypatch):
    monkeypatch.setenv("MODE", "invalid")
    with pytest.raises(SystemExit):
        venvalid({"MODE": ["dev", "prod", "test"]})


def test_allowed_invalid(monkeypatch):
    monkeypatch.setenv("REGION", "asia")
    with pytest.raises(SystemExit):
        venvalid({"REGION": (str, {"allowed": ["us", "eu"]})})


def test_invalid_cast(monkeypatch):
    monkeypatch.setenv("PORT", "not-a-number")
    with pytest.raises(SystemExit):
        venvalid({"PORT": int})


def test_failed_custom_validation(monkeypatch):
    monkeypatch.setenv("PORT", "80")
    with pytest.raises(SystemExit):
        venvalid({"PORT": (int, {"validate": lambda x: x >= 1024})})


def test_helpers_with_custom_source():
    config = venvalid(
        {
            "TIMEOUT": int_(default=30),
            "ENABLED": bool_(default=True),
            "ENV": str_(allowed=["dev", "prod"], default="dev"),
            "DECIMAL": decimal_(default=Decimal("1.1")),
            "START": datetime_(default=datetime(2025, 1, 1)),
            "SETTINGS": json_(default={}),
            "LOG_PATH": path_(default=Path("/tmp/log.txt")),
            "ALLOWED": list_(default=["a", "b"]),
        },
        source={
            "TIMEOUT": "60",
            "ENABLED": "false",
            "ENV": "prod",
            "DECIMAL": "2.5",
            "START": "2025-12-25T10:00:00",
            "SETTINGS": '{"key": "value"}',
            "LOG_PATH": "/var/log/app.log",
            "ALLOWED": "x.com, y.com , z.com",
        },
    )

    assert config["TIMEOUT"] == 60
    assert config["ENABLED"] is False
    assert config["ENV"] == "prod"
    assert config["DECIMAL"] == Decimal("2.5")
    assert config["START"] == datetime(2025, 12, 25, 10, 0, 0)
    assert config["SETTINGS"] == {"key": "value"}
    assert config["LOG_PATH"] == Path("/var/log/app.log")
    assert config["ALLOWED"] == ["x.com", "y.com", "z.com"]
