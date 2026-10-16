def test_mixed_case_no_whitespace():
    assert normalized_equal('ABC', 'abc') == True
