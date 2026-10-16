import numpy as np

def replace_negatives_with_zero(arr):
    return np.where(arr < 0, 0, arr)
