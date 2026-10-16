def test_keyword_only():
    result = logged_call(dict, a=1, b=2)
    assert result == {'a': 1, 'b': 2}
