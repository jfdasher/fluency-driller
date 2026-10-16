import numpy as np

def test_all_below_threshold():
    arr = np.array([1, 2, 3])
    result = fn(arr, 100)
    expected = np.array([False, False, False])
    assert result.dtype == bool
    np.testing.assert_array_equal(result, expected)
