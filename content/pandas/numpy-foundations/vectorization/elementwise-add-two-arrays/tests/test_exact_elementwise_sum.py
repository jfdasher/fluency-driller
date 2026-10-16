import numpy as np

def test_exact_elementwise_sum():
    a = np.array([1, 2, 3, 4])
    b = np.array([10, 20, 30, 40])
    result = fn(a, b)
    expected = np.array([11, 22, 33, 44])
    assert isinstance(result, np.ndarray)
    assert result.tolist() == expected.tolist()
