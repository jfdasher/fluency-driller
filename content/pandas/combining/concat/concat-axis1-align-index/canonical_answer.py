import pandas as pd

def concat_side_by_side(left, right):
    return pd.concat([left, right], axis=1)
