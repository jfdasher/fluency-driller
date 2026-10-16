import numpy as np

def test_all_non_negative_unchanged():
    arr = np.array([0, 1, 2, 100])
    result = fn(arr)
    np.testing.assert_array_equal(result, arr)
