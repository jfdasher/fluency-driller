import numpy as np

def test_input_not_mutated():
    arr = np.array([-5, 3, -2, 8])
    original = arr.copy()
    fn(arr)
    np.testing.assert_array_equal(arr, original)
