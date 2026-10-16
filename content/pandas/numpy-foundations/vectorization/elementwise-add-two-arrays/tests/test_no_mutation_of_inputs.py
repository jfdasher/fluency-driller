import numpy as np

def test_no_mutation_of_inputs():
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([4.0, 5.0, 6.0])
    a_orig = a.copy()
    b_orig = b.copy()
    fn(a, b)
    assert a.tolist() == a_orig.tolist()
    assert b.tolist() == b_orig.tolist()
