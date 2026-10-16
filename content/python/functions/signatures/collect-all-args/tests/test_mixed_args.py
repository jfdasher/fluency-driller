def test_mixed_args():
    result = collect_args('a', 'b', key='value', num=42)
    assert result == (('a', 'b'), {'key': 'value', 'num': 42})
