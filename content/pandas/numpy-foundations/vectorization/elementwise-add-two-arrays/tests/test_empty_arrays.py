import numpy as np

def test_empty_arrays():
    a = np.array([], dtype=float)
    b = np.array([], dtype=float)
    result = fn(a, b)
    assert isinstance(result, np.ndarray)
    assert len(result) == 0
