def test_empty_dataframe_index_name():
    import pandas as pd
    df = pd.DataFrame({'score': pd.Series([], dtype=int), 'grade': pd.Series([], dtype=str)})
    result = fn(df)
    assert result.index.name == 'student_id'
    assert len(result) == 0
