def test_input_dict_not_mutated():
    import pandas as pd
    data = {
        'name':  {'a': 'Alice', 'b': 'Bob',   'c': 'Carol'},
        'score': {'a': 90,      'b': 85,       'c': 95}
    }
    original_keys = set(data.keys())
    fn(data)
    assert set(data.keys()) == original_keys
    assert list(data['name'].keys()) == ['a', 'b', 'c']
