import pandas as pd
from pandas.testing import assert_frame_equal

def test_single_group():
    df = pd.DataFrame({
        'dept': ['X', 'X'],
        'salary': [40000, 60000],
        'years': [2, 4]
    })
    expected = pd.DataFrame({
        'avg_salary': [50000.0],
        'max_salary': [60000],
        'tenure': [3.0]
    }, index=pd.Index(['X'], name='dept'))
    assert_frame_equal(fn(df), expected)
