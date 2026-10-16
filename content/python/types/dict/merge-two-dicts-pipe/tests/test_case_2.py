def test_case_2():
    assert equal(merge_dicts_pipe(**{'a': {}, 'b': {'k': 5}}), {'k': 5})
