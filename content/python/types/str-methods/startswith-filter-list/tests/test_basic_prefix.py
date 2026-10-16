def test_basic_prefix():
    result = filter_by_prefix(['apple', 'apricot', 'banana', 'avocado'], 'ap')
    assert result == ['apple', 'apricot']
