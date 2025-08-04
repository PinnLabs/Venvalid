class EnvSafeError(Exception):
    def __init__(self, message: str):
        super().__init__(f"[venvalid] {message}")
