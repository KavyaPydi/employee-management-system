import os
from google.cloud import bigquery
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("BQ_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")
TABLE_REF = f"{PROJECT_ID}.{DATASET}.{TABLE}"

client = bigquery.Client()

# ----INSERT EMPLOYEE----
def add_employee(emp):
    query = f"""
        DECLARE new_id INT64;

        SET new_id = (
            SELECT IFNULL(MAX(employee_id), 0) + 1
            FROM `{TABLE_REF}`
        );
        INSERT INTO `{TABLE_REF}` (employee_id, name, age, salary)
        VALUES (new_id, @name, @age, @salary);
        SELECT new_id AS employee_id;
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("employee_id", "INT64", emp.employee_id),
            bigquery.ScalarQueryParameter("name", "STRING", emp.name),
            bigquery.ScalarQueryParameter("age", "INT64", emp.age),
            bigquery.ScalarQueryParameter("salary", "FLOAT64", emp.salary)
        ]
    )
    result = list(client.query(query, job_config=job_config).result())[0]
    new_employee_id = result["employee_id"]
    return {
        "status": "success",
        "message": f"Employee added successfully with id {new_employee_id}",
        "employee_id": new_employee_id
    }

# ----GET ALL EMPLOYEES----
def get_all_employees():
    query = f"SELECT employee_id, name, age, salary FROM `{TABLE_REF}`"
    rows = client.query(query).result()
    return [dict(row) for row in rows]

# ----DELETE EMPLOYEE----
def delete_employee_by_id(employee_id):
    query = f"DELETE FROM `{TABLE_REF}` WHERE employee_id=@employee_id"
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("employee_id", "INT64", employee_id)
        ]
    )
    client.query(query, job_config=job_config).result()
    return {"status": "deleted"}

# ----MEDIAN AGE----
def get_median_age():
    query = f"""
        SELECT APPROX_QUANTILES(age, 2)[OFFSET(1)] AS median_age
        FROM `{TABLE_REF}`
    """
    row = list(client.query(query).result())[0]
    return row["median_age"]

# ----MEDIAN SALARY----
def get_median_salary():
    query = f"""
        SELECT APPROX_QUANTILES(salary, 2)[OFFSET(1)] AS median_salary
        FROM `{TABLE_REF}`
    """

    # query = f""" SELECT PERCENTILE_CONT(value, 0.5) OVER() AS median_salary FROM `{TABLE_REF}` LIMIT 1 """

    row = list(client.query(query).result())[0]
    return row["median_salary"]
