def test_single_element_array():
    import numpy as np
    arr = np.array([99])
    expected = np.array([0])
    result = fn(arr)
    np.testing.assert_array_equal(result, expected)
