def first_non_none(values):
    for v in values:
        if v is not None:
            return v
    return None
