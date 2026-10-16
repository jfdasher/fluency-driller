import pandas as pd
from pandas.testing import assert_frame_equal

def test_exact_equality():
    df = pd.DataFrame({'phone': ['(212) 555-1234', '(415) 867-5309', '(312) 999-0000']})
    expected = pd.DataFrame({'area_code': ['212', '415', '312']})
    assert_frame_equal(fn(df), expected)
