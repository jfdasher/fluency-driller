def odd_cubes(n):
    return {x**3 for x in range(n) if x % 2 != 0}
