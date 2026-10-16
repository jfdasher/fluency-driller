def test_exact_values_and_index():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    top = pd.DataFrame({'name': ['Alice', 'Bob'], 'score': [85, 90]})
    bottom = pd.DataFrame({'name': ['Carol', 'Dave'], 'score': [78, 92]})
    expected = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Carol', 'Dave'],
        'score': [85, 90, 78, 92]
    })
    assert_frame_equal(fn(top, bottom), expected)
