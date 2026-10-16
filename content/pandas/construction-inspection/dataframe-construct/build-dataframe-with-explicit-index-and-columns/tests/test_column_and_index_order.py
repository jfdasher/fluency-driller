def test_column_and_index_order():
    import pandas as pd
    data = {
        'name':  {'a': 'Alice', 'b': 'Bob',   'c': 'Carol'},
        'score': {'a': 90,      'b': 85,       'c': 95}
    }
    result = fn(data)
    assert list(result.columns) == ['score', 'name']
    assert list(result.index) == ['c', 'a', 'b']
