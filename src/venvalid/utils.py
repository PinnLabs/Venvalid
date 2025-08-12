import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Optional, Type


def _cast(
    value: str, expected_type: Type, *, datetime_format: Optional[str] = None
) -> Any:
    v = value.strip()

    if expected_type is bool:
        truthy = {"1", "true", "yes", "on"}
        falsy = {"0", "false", "no", "off"}
        val_lower = v.lower()
        if val_lower in truthy:
            return True
        elif val_lower in falsy:
            return False
        else:
            raise ValueError(f"Invalid boolean value: {v}")

    if expected_type is list:
        if not v:
            return []
        if v.startswith("[") and v.endswith("]"):
            try:
                parsed = json.loads(v)
                if not isinstance(parsed, list):
                    raise ValueError(f"Expected list, got {type(parsed).__name__}")
                return parsed
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON for list: {v}") from e
        return [item.strip() for item in v.split(",")]

    if expected_type in (dict, list):
        try:
            parsed = json.loads(v)
            if not isinstance(parsed, expected_type):
                raise ValueError(
                    f"Expected {expected_type.__name__}, got {type(parsed).__name__}"
                )
            return parsed
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for {expected_type.__name__}: {v}") from e

    if expected_type is Path:
        return Path(v)

    if expected_type is Decimal:
        try:
            return Decimal(v)
        except Exception as e:
            raise ValueError(f"Invalid Decimal value: {v}") from e

    if expected_type is datetime:
        try:
            return datetime.fromisoformat(v)
        except ValueError:
            if datetime_format:
                try:
                    return datetime.strptime(v, datetime_format)
                except ValueError as e:
                    raise ValueError(f"Invalid datetime format: {v}") from e
            raise ValueError(f"Invalid ISO datetime: {v}")

    try:
        return expected_type(v)
    except Exception as e:
        raise ValueError(f"Cannot cast '{v}' to {expected_type.__name__}") from e
