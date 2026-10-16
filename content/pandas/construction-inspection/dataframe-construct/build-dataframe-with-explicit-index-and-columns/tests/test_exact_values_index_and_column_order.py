def test_exact_values_index_and_column_order():
    import pandas as pd
    from pandas.testing import assert_frame_equal
    data = {
        'name':  {'a': 'Alice', 'b': 'Bob',   'c': 'Carol'},
        'score': {'a': 90,      'b': 85,       'c': 95}
    }
    expected = pd.DataFrame(
        {'score': [95, 90, 85], 'name': ['Carol', 'Alice', 'Bob']},
        index=pd.Index(['c', 'a', 'b'])
    )
    assert_frame_equal(fn(data), expected)
