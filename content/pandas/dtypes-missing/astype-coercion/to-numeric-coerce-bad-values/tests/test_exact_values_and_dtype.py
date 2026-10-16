def test_exact_values_and_dtype():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'value': ['3', 'abc', '7', '?', '1.5']})
    expected = pd.DataFrame({'value': pd.array([3.0, np.nan, 7.0, np.nan, 1.5], dtype='float64')})
    assert_frame_equal(fn(df), expected)
