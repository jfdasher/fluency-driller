import numpy as np

def test_scale_array_no_mutation():
    arr = np.array([10, 20, 30])
    original = arr.copy()
    fn(arr, 5)
    assert np.array_equal(arr, original), 'Input array was mutated'
