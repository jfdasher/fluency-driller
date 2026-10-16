def test_both_need_strip_and_lower():
    assert normalized_equal('  PYTHON  ', '  python  ') == True
