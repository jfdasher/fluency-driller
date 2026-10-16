def test_from_csv_float_salary():
    e = Employee.from_csv('Bob,HR,52500.5')
    assert e.salary == 52500.5
    assert isinstance(e.salary, float)
