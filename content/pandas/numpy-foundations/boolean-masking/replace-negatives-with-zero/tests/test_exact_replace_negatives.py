import numpy as np

def test_exact_replace_negatives():
    arr = np.array([3, -1, 0, 4, -7, 2])
    result = fn(arr)
    expected = np.array([3, 0, 0, 4, 0, 2])
    np.testing.assert_array_equal(result, expected)
