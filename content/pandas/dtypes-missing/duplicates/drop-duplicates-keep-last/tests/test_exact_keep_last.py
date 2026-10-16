def test_exact_keep_last():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'city': ['NYC', 'LAX', 'NYC', 'LAX', 'CHI'],
        'temp': [70, 85, 72, 88, 60]
    })
    expected = pd.DataFrame(
        {'city': ['NYC', 'LAX', 'CHI'], 'temp': [72, 88, 60]},
        index=[2, 3, 4]
    )
    assert_frame_equal(fn(df), expected)
