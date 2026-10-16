def test_q3_absent_from_output():
    import pandas as pd
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Ada', 'Bob'],
        'q1': [10, 40],
        'q2': [20, 50],
        'q3': [30, 60]
    })
    result = fn(df)
    assert 'q3' not in result['quarter'].values, 'q3 should not appear in quarter column'
    assert 'q3' not in result.columns, 'q3 should not be a column'
