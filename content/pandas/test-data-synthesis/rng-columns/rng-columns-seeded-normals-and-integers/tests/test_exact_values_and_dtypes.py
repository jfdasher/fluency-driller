def test_exact_values_and_dtypes():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    rng = np.random.default_rng(seed=42)
    expected = pd.DataFrame({
        'score': rng.standard_normal(5),
        'count': rng.integers(0, 10, size=5).astype('int64')
    })
    result = fn()
    assert_frame_equal(result, expected, check_exact=False, rtol=1e-12)
