def test_case_4():
    assert equal(keys_with_value(**{'d': {'only': 42}, 'target': 42}), ['only'])
