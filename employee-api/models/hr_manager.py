from models.employee import Employee

class HRManager(Employee):
    def __init__(self, employee_id, name, age, salary, department):
        super().__init__(employee_id, name, age, salary)
        self.department = department

    def to_dict(self):
        data = super().to_dict()
        data.update({"department": self.department})
        return data
