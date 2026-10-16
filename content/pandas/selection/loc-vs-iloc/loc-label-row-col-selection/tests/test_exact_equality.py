def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame(
        {'x': [1, 4, 7, 10], 'y': [2, 5, 8, 11], 'z': [3, 6, 9, 12]},
        index=['a', 'b', 'c', 'd']
    )
    expected = pd.DataFrame(
        {'x': [4, 10], 'z': [6, 12]},
        index=['b', 'd']
    )
    assert_frame_equal(fn(df), expected)
