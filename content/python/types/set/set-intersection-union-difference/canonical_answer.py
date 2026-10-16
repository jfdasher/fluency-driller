def set_ops(a, b):
    sa, sb = set(a), set(b)
    return {
        'intersection': sorted(sa & sb),
        'union': sorted(sa | sb),
        'difference': sorted(sa - sb),
    }
