from src.venvalid.errors import EnvSafeError


def validate_env_var(name: str, value: str | None):
    if not value:
        raise EnvSafeError(f"Missing required environment variable: {name}")
    return True
