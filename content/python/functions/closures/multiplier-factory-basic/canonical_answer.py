def make_multiplier(factor):
    def multiplier(x):
        return x * factor
    return multiplier
