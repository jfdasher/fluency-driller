def test_direct_init_still_works():
    e = Employee('Dave', 'IT', 80000)
    assert e.name == 'Dave'
    assert e.department == 'IT'
    assert e.salary == 80000.0
