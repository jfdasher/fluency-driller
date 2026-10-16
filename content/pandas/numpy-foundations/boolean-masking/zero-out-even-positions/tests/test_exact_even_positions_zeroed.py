def test_exact_even_positions_zeroed():
    import numpy as np
    arr = np.array([10, 21, 30, 41, 50])
    expected = np.array([0, 21, 0, 41, 0])
    result = fn(arr)
    np.testing.assert_array_equal(result, expected)
