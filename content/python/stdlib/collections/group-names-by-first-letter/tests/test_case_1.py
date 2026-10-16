def test_case_1():
    assert equal(group_names_by_first_letter(**{'names': ['Zara', 'zoe', 'adam', 'Alice']}), {'Z': ['Zara', 'zoe'], 'A': ['Alice', 'adam']})
