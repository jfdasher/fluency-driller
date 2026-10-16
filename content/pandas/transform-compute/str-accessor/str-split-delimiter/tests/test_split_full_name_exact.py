import pandas as pd
from pandas.testing import assert_frame_equal

def test_split_full_name_exact():
    df = pd.DataFrame({'full_name': ['Alice Bob', 'Carol Dee', 'Eve Fox']})
    expected = pd.DataFrame({'first': ['Alice', 'Carol', 'Eve'], 'last': ['Bob', 'Dee', 'Fox']})
    assert_frame_equal(fn(df), expected)
