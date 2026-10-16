import numpy as np

def test_select_positive_exact():
    arr = np.array([-3, 0, 1, -1, 4, 2, 0, -5, 7])
    expected = np.array([1, 4, 2, 7])
    result = fn(arr)
    np.testing.assert_array_equal(result, expected)
