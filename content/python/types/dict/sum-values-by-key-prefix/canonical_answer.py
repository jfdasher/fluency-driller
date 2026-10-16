def filter_a_keys(d: dict) -> dict:
    return {k: v for k, v in d.items() if k.startswith('a')}
