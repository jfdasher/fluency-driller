def test_not_found_raises():
    import pytest
    with pytest.raises(ValueError):
        strict_find('hello world', 'xyz')
