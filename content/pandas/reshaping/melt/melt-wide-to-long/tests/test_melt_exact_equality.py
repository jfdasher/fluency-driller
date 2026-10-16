import pandas as pd
from pandas.testing import assert_frame_equal

def test_melt_exact_equality():
    df = pd.DataFrame({
        'student': ['Alice', 'Bob'],
        'q1': [85, 72],
        'q2': [90, 68],
        'q3': [78, 95]
    })
    expected = pd.DataFrame({
        'student': ['Alice', 'Bob', 'Alice', 'Bob', 'Alice', 'Bob'],
        'quarter': ['q1', 'q1', 'q2', 'q2', 'q3', 'q3'],
        'score': [85, 72, 90, 68, 78, 95]
    })
    expected['student'] = expected['student'].astype('object')
    expected['quarter'] = expected['quarter'].astype('object')
    expected['score'] = expected['score'].astype('int64')
    result = fn(df)
    assert_frame_equal(result.reset_index(drop=True), expected.reset_index(drop=True), check_like=False)
