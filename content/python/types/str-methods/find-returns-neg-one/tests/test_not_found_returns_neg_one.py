def test_not_found_returns_neg_one():
    assert safe_find('hello world', 'xyz') == -1
