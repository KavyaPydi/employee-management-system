import os
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError, NotFound, BadRequest
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.getenv("BQ_PROJECT_ID")
DATASET = os.getenv("BQ_DATASET")
TABLE = os.getenv("BQ_TABLE")
TABLE_REF = f"{PROJECT_ID}.{DATASET}.{TABLE}"

client = bigquery.Client()

# ----INSERT EMPLOYEE----
def add_employee(emp):
    try:
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
                bigquery.ScalarQueryParameter("name", "STRING", emp.name),
                bigquery.ScalarQueryParameter("age", "INT64", emp.age),
                bigquery.ScalarQueryParameter("salary", "FLOAT64", emp.salary),
            ]
        )

        job = client.query(query, job_config=job_config)
        result = list(job.result())[0]
        new_employee_id = result["employee_id"]

        return {
            "status": "success",
            "message": f"Employee added successfully with id {new_employee_id}",
            "employee_id": new_employee_id
        }

    except BadRequest as e:
        print(f"Query error: {e}")
        return {"status": "error", "message": str(e)}

    except GoogleAPIError as e:
        print(f"BigQuery API error: {e}")
        return {"status": "error", "message": "BigQuery API error occurred."}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"status": "error", "message": "An unexpected error occurred."}


# ----GET ALL EMPLOYEES----
def get_all_employees():
    try:
        query = f"SELECT employee_id, name, age, salary FROM `{TABLE_REF}` ORDER BY employee_id ASC"
        rows = client.query(query).result()
        return [dict(row) for row in rows]

    except NotFound:
        return {"status": "error", "message": "Table not found."}

    except GoogleAPIError as e:
        print(f"BigQuery error: {e}")
        return {"status": "error", "message": "Failed to retrieve employees."}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"status": "error", "message": "Unexpected error occurred."}


# ----DELETE EMPLOYEE----
def delete_employee_by_id(employee_id):
    try:
        query = f"DELETE FROM `{TABLE_REF}` WHERE employee_id = @employee_id"
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter("employee_id", "INT64", employee_id)
            ]
        )
        client.query(query, job_config=job_config).result()
        return {"status": "success", "message": "Employee deleted"}

    except NotFound:
        return {"status": "error", "message": "Employee or table not found."}

    except GoogleAPIError as e:
        print(f"BigQuery error: {e}")
        return {"status": "error", "message": "Failed to delete employee."}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"status": "error", "message": "Unexpected error occurred."}


# ----MEDIAN AGE----
def get_median_age():
    try:
        query = f"""
            SELECT APPROX_QUANTILES(age, 2)[OFFSET(1)] AS median_age
            FROM `{TABLE_REF}`
        """
        row = list(client.query(query).result())[0]
        return row["median_age"]

    except GoogleAPIError as e:
        print(f"BigQuery error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# ----MEDIAN SALARY----
def get_median_salary():
    try:
        query = f"""
            SELECT APPROX_QUANTILES(salary, 2)[OFFSET(1)] AS median_salary
            FROM `{TABLE_REF}`
        """

        row = list(client.query(query).result())[0]
        return row["median_salary"]

    except GoogleAPIError as e:
        print(f"BigQuery error: {e}")
        return None

    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
