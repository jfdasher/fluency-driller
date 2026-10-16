import pandas as pd

def test_melt_output_shape_and_columns():
    df = pd.DataFrame({
        'student': ['Alice', 'Bob'],
        'q1': [85, 72],
        'q2': [90, 68],
        'q3': [78, 95]
    })
    result = fn(df)
    assert list(result.columns) == ['student', 'quarter', 'score'], 'Columns must be student, quarter, score in order'
    assert len(result) == 6, 'Melting 2 students x 3 quarters should give 6 rows'
    assert set(result['quarter'].unique()) == {'q1', 'q2', 'q3'}, 'quarter column must contain q1, q2, q3'
