def test_case_4():
    assert equal(merge_dicts_unpack(**{'a': {'p': 1, 'q': 2}, 'b': {'p': 42}}), {'p': 42, 'q': 2})
