import os
from typing import Optional

from rich.console import Console

from .dotenv import load_env_file
from .errors import EnvSafeError
from .utils import _cast


def venvalid(
    specs: dict[str, object],
    *,
    source: Optional[dict[str, str]] = None,
    dotenv_path: str = ".env",
    dotenv_override: bool = False,
    pretty: bool = False,
    exit_on_error: bool = True,
) -> dict[str, object]:
    """
    Validates and loads environment variables based on declarative specifications.

    Args:
        specs (dict): Variable specifications (type, default, etc).
        source (dict, optional): Alternative source for the variables (default: os.environ).
        dotenv_path (str, optional): Path to the .env file to be loaded.
        dotenv_override (bool): If True, overwrites existing variables when loading .env.
        pretty (bool): If True, uses rich to pretty-print errors.
        exit_on_error (bool): If True, calls SystemExit(1) on validation errors (default=True for backwards compat).

    Returns:
        dict: Validated and converted environment variables.
    """
    if source is None:
        load_env_file(dotenv_path, override=dotenv_override)

    env_source = source or os.environ
    result: dict[str, object] = {}

    for key, spec in specs.items():
        raw_value = env_source.get(key)
        try:
            value = _resolve_variable(key, raw_value, spec)
            result[key] = value
        except EnvSafeError as e:
            if pretty:
                try:
                    console = Console()
                    console.print(f"[bold red]Error:[/bold red] {e}")
                except ImportError:
                    pass
            if exit_on_error:
                raise SystemExit(1)
            raise

    return result


def _resolve_variable(key: str, raw: str | None, spec: object) -> object:
    """
    Resolves and validates an environment variable based on its specification.
    """
    if isinstance(spec, list):
        if raw is None:
            raise EnvSafeError(f"{key} is required and must be one of {spec}")
        if raw not in spec:
            raise EnvSafeError(f"{key} must be one of {spec}, but got '{raw}'")
        return raw

    expected_type: type
    default = None
    allowed = None
    validate = None

    if isinstance(spec, tuple):
        t_candidate, options = spec
        if not isinstance(t_candidate, type):
            raise TypeError(f"{key}: expected a type, got {t_candidate}")
        expected_type = t_candidate
        default = options.get("default")
        allowed = options.get("allowed")
        validate = options.get("validate")
    elif isinstance(spec, type):
        expected_type = spec
    else:
        raise TypeError(f"{key}: invalid spec type {type(spec)}")

    if raw is None:
        if default is not None:
            return default
        raise EnvSafeError(f"Missing required environment variable: {key}")

    try:
        parsed = _cast(raw, expected_type)
    except ValueError as ve:
        type_name = getattr(expected_type, "__name__", str(expected_type))
        raise EnvSafeError(
            f"Invalid value for {key}: expected {type_name}, got '{raw}'"
        ) from ve

    if allowed is not None and parsed not in allowed:
        raise EnvSafeError(f"{key} must be one of {allowed}, but got '{parsed}'")

    if validate is not None and not validate(parsed):
        raise EnvSafeError(f"{key} failed custom validation with value '{parsed}'")

    return parsed
