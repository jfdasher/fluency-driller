class Employee:
    def __init__(self, name, department, salary):
        self.name = name
        self.department = department
        self.salary = float(salary)

    @classmethod
    def from_csv(cls, csv_row):
        name, department, salary = csv_row.split(',')
        return cls(name, department, float(salary))
