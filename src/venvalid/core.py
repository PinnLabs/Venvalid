import os

from src.venvalid.errors import EnvSafeError


def env(
    specs: dict[str, object], *, source: dict[str, str] | None = None
) -> dict[str, object]:
    env_source = source or os.environ
    result: dict[str, object] = {}

    for key, spec in specs.items():
        raw_value = env_source.get(key)

        try:
            value = _resolve_variable(key, raw_value, spec)
            result[key] = value
        except EnvSafeError as e:
            print(f"\n{e}\n")
            raise SystemExit(1)

    return result


def _resolve_variable(key: str, raw: str | None, spec: object) -> object:
    from .utils import _cast

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
