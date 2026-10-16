def test_uppercase_name_exact():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({'name': ['alice', 'bob', 'carol'], 'score': [85, 92, 78]})
    expected = pd.DataFrame({'name': ['ALICE', 'BOB', 'CAROL'], 'score': [85, 92, 78]})
    assert_frame_equal(fn(df), expected)
