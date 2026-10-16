def get_processed(d, key):
    try:
        value = d[key]
    except KeyError:
        return None
    else:
        return value.upper()
