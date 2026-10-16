def split_on_first(s, sep):
    before, found, after = s.partition(sep)
    return (before, after)
