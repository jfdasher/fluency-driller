def sort_keys_by_value_ascending(d):
    return sorted(d, key=lambda k: (d[k], k))
