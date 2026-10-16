import pandas as pd
from pandas.testing import assert_frame_equal

def test_exact_values():
    df = pd.DataFrame({
        'dept': ['A', 'A', 'B', 'B'],
        'salary': [50000, 60000, 70000, 80000],
        'years': [3, 5, 7, 9]
    })
    expected = pd.DataFrame({
        'avg_salary': [55000.0, 75000.0],
        'max_salary': [60000, 80000],
        'tenure': [4.0, 8.0]
    }, index=pd.Index(['A', 'B'], name='dept'))
    assert_frame_equal(fn(df), expected)
