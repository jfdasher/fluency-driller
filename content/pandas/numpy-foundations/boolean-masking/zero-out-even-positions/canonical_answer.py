import numpy as np

def zero_out_even_positions(arr: np.ndarray) -> np.ndarray:
    out = arr.copy()
    mask = np.zeros(len(arr), dtype=bool)
    mask[::2] = True
    out[mask] = 0
    return out
