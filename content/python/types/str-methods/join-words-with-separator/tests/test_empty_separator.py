def test_empty_separator():
    assert join_words(['foo', 'bar', 'baz'], '') == 'foobarbaz'
