def test_dtypes():
    import numpy as np
    result = fn()
    assert result['score'].dtype == np.float64, f"'score' dtype should be float64, got {result['score'].dtype}"
    assert result['count'].dtype == np.int64, f"'count' dtype should be int64, got {result['count'].dtype}"
