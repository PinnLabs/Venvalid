import pytest

from src.venvalid.errors import EnvSafeError
from src.venvalid.validator import validate_env_var


def test_validate_env_var_success():
    assert validate_env_var("API_KEY", "secret") is True


def test_validate_env_var_missing():
    with pytest.raises(EnvSafeError) as exc_info:
        validate_env_var("API_KEY", None)

    assert "Missing required environment variable: API_KEY" in str(exc_info.value)
