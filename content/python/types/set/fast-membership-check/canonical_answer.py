def is_allowed(allowed: list, username: str) -> bool:
    allowed_set = set(allowed)
    return username in allowed_set
