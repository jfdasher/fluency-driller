def test_does_not_mutate_original():
    original = [(3, 0), (1, 0), (2, 0)]
    result = lex_sort(original)
    assert original == [(3, 0), (1, 0), (2, 0)]
    assert result == [(1, 0), (2, 0), (3, 0)]
