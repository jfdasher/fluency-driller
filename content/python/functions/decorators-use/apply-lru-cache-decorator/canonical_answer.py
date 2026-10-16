import functools

@functools.lru_cache(maxsize=None)
def slow_square(n):
    return n * n
