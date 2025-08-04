import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path


def _cast(value: str, expected_type: type) -> object:
    v = value.strip()

    if expected_type is bool:
        return v.lower() in ("1", "true", "yes", "on")
    if expected_type is list:
        return [item.strip() for item in v.split(",")]
    if expected_type is dict:
        try:
            return json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for dict: {v}") from e
    if expected_type is Path:
        return Path(v)
    if expected_type is Decimal:
        return Decimal(v)
    if expected_type is datetime:
        try:
            return datetime.fromisoformat(v)
        except ValueError as e:
            raise ValueError(f"Invalid ISO datetime: {v}") from e
    return expected_type(v)
