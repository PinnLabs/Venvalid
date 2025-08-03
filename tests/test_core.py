import pytest

from src.venvalid.core import env


def test_basic_types(monkeypatch):
    monkeypatch.setenv("DEBUG", "true")
    monkeypatch.setenv("PORT", "8000")
    monkeypatch.setenv("SECRET_KEY", "abc123")

    config = env(
        {
            "DEBUG": bool,
            "PORT": int,
            "SECRET_KEY": str,
        }
    )

    assert config["DEBUG"] is True
    assert config["PORT"] == 8000
    assert config["SECRET_KEY"] == "abc123"


def test_default_values(monkeypatch):
    monkeypatch.delenv("ENV", raising=False)

    config = env({"ENV": (str, {"default": "development"})})

    assert config["ENV"] == "development"


def test_enum_values(monkeypatch):
    monkeypatch.setenv("MODE", "prod")

    config = env({"MODE": ["dev", "prod", "test"]})

    assert config["MODE"] == "prod"


def test_enum_invalid(monkeypatch):
    monkeypatch.setenv("MODE", "invalid")

    with pytest.raises(SystemExit):
        env({"MODE": ["dev", "prod", "test"]})


def test_allowed_values(monkeypatch):
    monkeypatch.setenv("REGION", "us")

    config = env({"REGION": (str, {"allowed": ["us", "eu"]})})

    assert config["REGION"] == "us"


def test_allowed_invalid(monkeypatch):
    monkeypatch.setenv("REGION", "asia")

    with pytest.raises(SystemExit):
        env({"REGION": (str, {"allowed": ["us", "eu"]})})


def test_list_type(monkeypatch):
    monkeypatch.setenv("ALLOWED_HOSTS", "a.com,b.com , c.com")

    config = env({"ALLOWED_HOSTS": list})

    assert config["ALLOWED_HOSTS"] == ["a.com", "b.com", "c.com"]


def test_missing_required(monkeypatch):
    monkeypatch.delenv("MISSING", raising=False)

    with pytest.raises(SystemExit):
        env({"MISSING": str})


def test_bool_variants(monkeypatch):
    monkeypatch.setenv("FEATURE_A", "yes")
    monkeypatch.setenv("FEATURE_B", "false")

    config = env(
        {
            "FEATURE_A": bool,
            "FEATURE_B": bool,
        }
    )

    assert config["FEATURE_A"] is True
    assert config["FEATURE_B"] is False
