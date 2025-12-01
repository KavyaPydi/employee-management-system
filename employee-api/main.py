from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from models.employee import Employee
from db.db_utils import (
    add_employee, get_all_employees,
    delete_employee_by_id, get_median_age,
    get_median_salary
)

app = FastAPI(title="Employee Management API")

class EmployeeRequest(BaseModel):
    employee_id: Optional[int] = None
    name: str
    age: int
    salary: float

# POST /employee
@app.post("/employee")
def create_employee(emp: EmployeeRequest):

    result = add_employee(emp)
    return result

# GET /employees
@app.get("/employees")
def list_employees():
    return get_all_employees()

# DELETE /employee/{id}
@app.delete("/employee/{id}")
def delete_employee(id: int):
    return delete_employee_by_id(id)


# GET /stats/median-age
@app.get("/stats/median-age")
def median_age():
    return {"median_age": get_median_age()}


# GET /stats/median-salary
@app.get("/stats/median-salary")
def median_salary():
    return {"median_salary": get_median_salary()}
