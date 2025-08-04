import os
from pathlib import Path


def load_env_file(filepath: str = ".env", override: bool = False) -> None:
    """
    Loads environment variables from an .env file into os.environ.

    Args:
        filepath (str): Path of the .env file.
        override (bool): If True, overwrites variables already in os.environ.
    """
    path = Path(filepath)

    if not path.is_file():
        return

    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if override or key not in os.environ:
                os.environ[key] = value
