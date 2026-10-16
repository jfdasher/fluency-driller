import numpy as np

def test_select_positive_all_nonpositive():
    arr = np.array([-1, -2, 0, -3])
    result = fn(arr)
    np.testing.assert_array_equal(result, np.array([], dtype=arr.dtype))
