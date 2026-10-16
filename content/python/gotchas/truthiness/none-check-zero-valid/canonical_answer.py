def get_value(data, key, default):
    val = data.get(key)
    if val is not None:
        return val
    return default
