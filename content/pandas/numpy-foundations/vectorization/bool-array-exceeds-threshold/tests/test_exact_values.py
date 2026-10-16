import numpy as np

def test_exact_values():
    arr = np.array([1, 5, 3, 8, 2])
    threshold = 4
    result = fn(arr, threshold)
    expected = np.array([False, True, False, True, False])
    assert result.dtype == bool
    assert result.shape == expected.shape
    np.testing.assert_array_equal(result, expected)
