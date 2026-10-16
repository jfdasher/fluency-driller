def test_plain_types_unchanged():
    import json
    data = {'x': 1, 'y': [2, 3], 'z': 'hello'}
    result = fn(data)
    assert json.loads(result) == data
