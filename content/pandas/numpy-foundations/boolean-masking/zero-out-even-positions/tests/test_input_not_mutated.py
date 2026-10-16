def test_input_not_mutated():
    import numpy as np
    arr = np.array([10, 21, 30, 41, 50])
    original = arr.copy()
    fn(arr)
    np.testing.assert_array_equal(arr, original)
