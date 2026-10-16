def test_empty_dataframe_reset_index():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame(
        {'score': pd.Series([], dtype=int)},
        index=pd.Index([], name='name', dtype=object)
    )
    result = fn(df)
    expected = pd.DataFrame({
        'name': pd.Series([], dtype=object),
        'score': pd.Series([], dtype=int)
    })
    assert_frame_equal(result, expected)
