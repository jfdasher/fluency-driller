def keys_with_value(d: dict, target: int) -> list:
    return sorted(k for k, v in d.items() if v == target)
