import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

def test_exact_equality():
    df = pd.DataFrame({
        'a': [1.0, 2.0, 3.0, np.nan],
        'b': [np.nan, 5.0, 6.0, np.nan],
        'c': [7.0, 8.0, 9.0, 10.0],
        'd': [np.nan, np.nan, np.nan, np.nan],
    })
    expected = pd.DataFrame({
        'a': [1.0, 2.0, 3.0, np.nan],
        'c': [7.0, 8.0, 9.0, 10.0],
    })
    assert_frame_equal(fn(df), expected)
