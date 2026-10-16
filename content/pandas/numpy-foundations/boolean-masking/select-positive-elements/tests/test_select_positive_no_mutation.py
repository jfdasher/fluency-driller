import numpy as np

def test_select_positive_no_mutation():
    arr = np.array([-3, 0, 1, -1, 4, 2, 0, -5, 7])
    original = arr.copy()
    fn(arr)
    np.testing.assert_array_equal(arr, original)
