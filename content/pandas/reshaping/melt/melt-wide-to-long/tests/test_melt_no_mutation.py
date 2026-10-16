import pandas as pd

def test_melt_no_mutation():
    df = pd.DataFrame({
        'student': ['Alice', 'Bob'],
        'q1': [85, 72],
        'q2': [90, 68],
        'q3': [78, 95]
    })
    original_cols = list(df.columns)
    fn(df)
    assert list(df.columns) == original_cols, 'Input df should not be mutated'
    assert len(df) == 2, 'Input df row count should be unchanged'
