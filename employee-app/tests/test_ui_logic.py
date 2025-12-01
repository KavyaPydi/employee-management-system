import pytest
from unittest.mock import patch
from streamlit_app import (
    api_add_employee,
    api_get_employees,
    api_delete_employee,
    api_get_stats
)


# --------------------------------------------
# Test Add Employee API Wrapper
# --------------------------------------------
@patch("streamlit_app.requests.post")
def test_api_add_employee(mock_post):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "success"}

    response, code = api_add_employee("John", 30, 5000)

    assert code == 200
    assert response["status"] == "success"
    mock_post.assert_called_once()


# --------------------------------------------
# Test Get Employees API Wrapper
# --------------------------------------------
@patch("streamlit_app.requests.get")
def test_api_get_employees(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"employee_id": "E001", "name": "John", "age": 30, "salary": 5000}
    ]

    response, code = api_get_employees()

    assert code == 200
    assert isinstance(response, list)
    assert response[0]["employee_id"] == "E001"


# --------------------------------------------
# Test Delete Employee Wrapper
# --------------------------------------------
@patch("streamlit_app.requests.delete")
def test_api_delete_employee(mock_del):
    mock_del.return_value.status_code = 200
    mock_del.return_value.json.return_value = {"status": "deleted"}

    response, code = api_delete_employee("E001")

    assert code == 200
    assert response["status"] == "deleted"


# --------------------------------------------
# Test Stats API Wrapper
# --------------------------------------------
@patch("streamlit_app.requests.get")
def test_api_stats(mock_get):
    # first call: median-age
    mock_get.side_effect = [
        MockResp({"median_age": 35}),
        MockResp({"median_salary": 70000}),
    ]

    age, salary = api_get_stats()

    assert age == 35
    assert salary == 70000


# Helper class to simulate Response.json()
class MockResp:
    def __init__(self, json_data):
        self._json = json_data

    def json(self):
        return self._json
