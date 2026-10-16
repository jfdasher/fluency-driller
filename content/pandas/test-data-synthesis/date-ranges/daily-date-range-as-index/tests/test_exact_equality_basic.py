def test_exact_equality_basic():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal

    result = fn('2024-01-01', 3)

    idx = pd.date_range(start='2024-01-01', periods=3, freq='D', name='date')
    expected = pd.DataFrame({'value': [0, 1, 2]}, index=idx)

    assert_frame_equal(result, expected)
