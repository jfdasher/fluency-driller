def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'category': ['A', 'B', 'C', 'D', 'B', 'A'], 'value': [10, 20, 30, 40, 50, 60]})
    expected = pd.DataFrame({'category': ['B', 'D', 'B'], 'value': [20, 40, 50]}, index=[1, 3, 4])
    assert_frame_equal(fn(df).reset_index(drop=False), expected.reset_index(drop=False))
