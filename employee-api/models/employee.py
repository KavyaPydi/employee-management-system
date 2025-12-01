from models.person import Person

class Employee(Person):
    def __init__(self, employee_id: int, name: str, age: int, salary: float):
        super().__init__(name, age)
        self.employee_id = employee_id
        self.salary = salary

    def to_dict(self):
        data = super().to_dict()
        data.update({"employee_id": self.employee_id, "salary": self.salary})
        return data
