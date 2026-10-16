def test_basic():
    result = unique_first_chars(['apple', 'avocado', 'banana', 'cherry'])
    assert result == {'a', 'b', 'c'}
