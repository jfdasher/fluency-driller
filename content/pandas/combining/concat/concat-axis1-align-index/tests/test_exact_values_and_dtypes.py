def test_exact_values_and_dtypes():
    import pandas as pd
    import numpy as np
    from pandas.testing import assert_frame_equal
    left = pd.DataFrame({'val_a': [1, 2, 3]}, index=['a', 'b', 'c'])
    right = pd.DataFrame({'val_b': [20, 30, 40]}, index=['b', 'c', 'd'])
    result = fn(left, right)
    expected = pd.DataFrame(
        {'val_a': [1.0, 2.0, 3.0, np.nan], 'val_b': [np.nan, 20.0, 30.0, 40.0]},
        index=['a', 'b', 'c', 'd']
    )
    assert_frame_equal(result, expected)
