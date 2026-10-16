def test_set_multiindex_index_names():
    import pandas as pd
    df = pd.DataFrame({
        'dept': ['eng'],
        'emp_id': [101],
        'salary': [90000]
    })
    result = fn(df)
    assert isinstance(result.index, pd.MultiIndex)
    assert result.index.names == ['dept', 'emp_id']
    assert list(result.columns) == ['salary']
