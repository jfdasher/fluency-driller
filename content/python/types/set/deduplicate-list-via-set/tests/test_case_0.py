def test_case_0():
    assert equal(deduplicate_list(**{'nums': [1, 2, 2, 3, 3, 3]}), [1, 2, 3])
