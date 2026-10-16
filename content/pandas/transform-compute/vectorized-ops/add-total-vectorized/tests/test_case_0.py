import pandas as pd
from pandas.testing import assert_frame_equal


def test_case_0():
    df = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30]})
    expected = pd.DataFrame({"a": [1, 2, 3], "b": [10, 20, 30], "total": [11, 22, 33]})
    assert_frame_equal(fn(df), expected)
