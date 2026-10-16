def test_case_4():
    assert equal(merge_dicts_pipe(**{'a': {'a': 1, 'b': 2}, 'b': {'a': 99}}), {'a': 99, 'b': 2})
