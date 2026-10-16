import numpy as np

def test_no_mutation():
    arr = np.array([10, 20, 30])
    original = arr.copy()
    fn(arr, 15)
    np.testing.assert_array_equal(arr, original)
