def test_exact_equality():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    df = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Alice', 'Carol', 'Bob', 'Carol'],
        'score': [90, 85, 90, 78, 85, 78]
    })
    expected = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Carol'],
        'score': [90, 85, 78]
    }, index=[0, 1, 3])
    assert_frame_equal(fn(df), expected)
