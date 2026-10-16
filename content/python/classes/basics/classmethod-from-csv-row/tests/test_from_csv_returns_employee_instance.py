def test_from_csv_returns_employee_instance():
    e = Employee.from_csv('Carol,Finance,70000')
    assert isinstance(e, Employee)
