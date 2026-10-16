import numpy as np

def test_scale_array_exact():
    arr = np.array([1, 2, 3, 4, 5])
    result = fn(arr, 3)
    expected = np.array([3, 6, 9, 12, 15])
    assert np.array_equal(result, expected), f'Expected {expected}, got {result}'
