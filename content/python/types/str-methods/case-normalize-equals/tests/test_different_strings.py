def test_different_strings():
    assert normalized_equal('  World ', 'word') == False
