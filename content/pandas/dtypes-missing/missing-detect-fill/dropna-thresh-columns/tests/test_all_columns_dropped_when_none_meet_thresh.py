import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

def test_all_columns_dropped_when_none_meet_thresh():
    df = pd.DataFrame({
        'x': [1.0, np.nan, np.nan],
        'y': [np.nan, np.nan, np.nan],
    })
    result = fn(df)
    assert result.shape == (3, 0)
