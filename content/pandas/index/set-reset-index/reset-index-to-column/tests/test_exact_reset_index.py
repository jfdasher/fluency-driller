def test_exact_reset_index():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame(
        {'score': [85, 92, 78]},
        index=pd.Index(['Alice', 'Bob', 'Carol'], name='name')
    )
    expected = pd.DataFrame({
        'name': pd.Series(['Alice', 'Bob', 'Carol'], dtype=object),
        'score': pd.Series([85, 92, 78], dtype=int)
    })
    assert_frame_equal(fn(df), expected)
