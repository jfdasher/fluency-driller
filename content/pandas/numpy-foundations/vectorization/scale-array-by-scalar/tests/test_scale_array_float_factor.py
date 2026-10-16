import numpy as np

def test_scale_array_float_factor():
    arr = np.array([2.0, 4.0, 6.0])
    result = fn(arr, 0.5)
    expected = np.array([1.0, 2.0, 3.0])
    assert np.allclose(result, expected), f'Expected {expected}, got {result}'
