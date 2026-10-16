import pandas as pd
from pandas.testing import assert_frame_equal

def test_split_full_name_single_row():
    df = pd.DataFrame({'full_name': ['Jane Doe']})
    expected = pd.DataFrame({'first': ['Jane'], 'last': ['Doe']})
    assert_frame_equal(fn(df), expected)
