def test_returns_set():
    result = unique_first_chars(['hello', 'world'])
    assert isinstance(result, set)
