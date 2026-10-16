def test_case_1():
    assert equal(merge_dicts_unpack(**{'a': {'name': 'Bob'}, 'b': {'city': 'Paris'}}), {'name': 'Bob', 'city': 'Paris'})
