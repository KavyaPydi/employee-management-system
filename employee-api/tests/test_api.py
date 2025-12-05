import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from main import app
from db import db_utils

client = TestClient(app)

# -------------------------
# Mock Data
# -------------------------
mock_employee = {
    "employee_id": 1,
    "name": "John Doe",
    "age": 30,
    "salary": 50000.0
}

mock_employees_list = [
    {"employee_id": 1, "name": "John Doe", "age": 30, "salary": 50000.0},
    {"employee_id": 2, "name": "Jane Smith", "age": 40, "salary": 60000.0},
]

# -------------------------
# POST /employee
# -------------------------
@patch("db.db_utils.client.query")
def test_create_employee(mock_query):
    # Mock BigQuery result
    mock_query.return_value.result.return_value = [{"employee_id": 1}]
    
    response = client.post("/employee", json={
        "name": "John Doe",
        "age": 30,
        "salary": 50000.0
    })

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["employee_id"] == 1
    assert "Employee added successfully" in data["message"]

# -------------------------
# GET /employees
# -------------------------
@patch("db.db_utils.client.query")
def test_list_employees(mock_query):
    # Mock BigQuery result
    mock_query.return_value.result.return_value = [
        {"employee_id": 1, "name": "John Doe", "age": 30, "salary": 50000.0},
        {"employee_id": 2, "name": "Jane Smith", "age": 40, "salary": 60000.0},
    ]

    # Patch dict(row) to just return the row itself
    with patch("db.db_utils.get_all_employees", wraps=db_utils.get_all_employees) as mock_func:
        response = client.get("/employees")
        assert response.status_code == 200
        assert response.json() == [
            {"employee_id": 1, "name": "John Doe", "age": 30, "salary": 50000.0},
            {"employee_id": 2, "name": "Jane Smith", "age": 40, "salary": 60000.0},
        ]


# -------------------------
# DELETE /employee/{id}
# -------------------------
@patch("db.db_utils.client.query")
def test_delete_employee(mock_query):
    mock_query.return_value.result.return_value = None
    response = client.delete("/employee/1")
    assert response.status_code == 200
    assert response.json() == {"status": "deleted"}

# -------------------------
# GET /stats/median-age
# -------------------------
@patch("db.db_utils.client.query")
def test_median_age(mock_query):
    mock_query.return_value.result.return_value = [{"median_age": 35}]
    response = client.get("/stats/median-age")
    assert response.status_code == 200
    assert response.json() == {"median_age": 35}

# -------------------------
# GET /stats/median-salary
# -------------------------
@patch("db.db_utils.client.query")
def test_median_salary(mock_query):
    mock_query.return_value.result.return_value = [{"median_salary": 55000.0}]
    response = client.get("/stats/median-salary")
    assert response.status_code == 200
    assert response.json() == {"median_salary": 55000.0}
