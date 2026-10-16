def test_case_3():
    assert equal(merge_dicts_unpack(**{'a': {'m': 7}, 'b': {}}), {'m': 7})
