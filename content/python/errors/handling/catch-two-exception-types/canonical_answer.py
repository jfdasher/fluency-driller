def safe_parse(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None
