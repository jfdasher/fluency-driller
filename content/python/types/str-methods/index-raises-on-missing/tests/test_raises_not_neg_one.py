def test_raises_not_neg_one():
    result = None
    try:
        result = strict_find('abcdef', 'zzz')
    except ValueError:
        result = 'raised'
    assert result == 'raised'
