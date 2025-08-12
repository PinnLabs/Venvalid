class ValidationError(Exception):
    pass


class EnvSafeError(ValidationError):
    def __init__(self, message: str):
        super().__init__(f"[venvalid] {message}")
