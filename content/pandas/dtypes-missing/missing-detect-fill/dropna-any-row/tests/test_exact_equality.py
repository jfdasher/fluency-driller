def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'a': [1.0, float('nan'), 7.0, 10.0],
        'b': [2.0, 5.0, float('nan'), 11.0],
        'c': [3.0, 6.0, 9.0, 12.0],
    })
    expected = pd.DataFrame(
        {'a': [1.0, 10.0], 'b': [2.0, 11.0], 'c': [3.0, 12.0]},
        index=[0, 3]
    )
    assert_frame_equal(fn(df), expected)
