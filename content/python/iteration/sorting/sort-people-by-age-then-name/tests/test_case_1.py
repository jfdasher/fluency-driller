def test_case_1():
    assert equal(sort_people_by_age_then_name(**{'people': [['Zara', 22], ['Amy', 22], ['Mike', 19]]}), [['Mike', 19], ['Amy', 22], ['Zara', 22]])
