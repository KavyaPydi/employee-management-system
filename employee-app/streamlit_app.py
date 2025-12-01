import streamlit as st
import requests
import pandas as pd

API_BASE = "http://localhost:8000"


# -------------------------------------
# Utility Functions to Call API
# -------------------------------------
def api_add_employee(name, age, salary):
    try:
        resp = requests.post(
            f"{API_BASE}/employee",
            json={"name": name, "age": age, "salary": salary},
            timeout=5
        )
        return resp.json(), resp.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def api_get_employees():
    try:
        resp = requests.get(f"{API_BASE}/employees", timeout=5)
        return resp.json(), resp.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def api_delete_employee(employee_id):
    try:
        resp = requests.delete(f"{API_BASE}/employee/{employee_id}", timeout=5)
        return resp.json(), resp.status_code
    except Exception as e:
        return {"error": str(e)}, 500


def api_get_stats():
    try:
        age_resp = requests.get(f"{API_BASE}/stats/median-age", timeout=5)
        salary_resp = requests.get(f"{API_BASE}/stats/median-salary", timeout=5)
        return (
            age_resp.json().get("median_age"),
            salary_resp.json().get("median_salary"),
        )
    except Exception as e:
        return None, None


# -------------------------------------
# Streamlit UI Layout
# -------------------------------------

# -------------------------
# Page Title
# -------------------------
st.set_page_config(page_title="Employee Dashboard", layout="wide")
# Custom CSS Styling
st.markdown("""
    <style>

    /* Card-like sections */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #d9e3f1 !important;
    }

    body {
        background-color: #e9edf4 !important;
    }
            
    h1 {
        color: #0e3b57 !important;
        font-weight: 700 !important;
        text-align: center;
    }
            
    h2, h3, h4, h5, h6, label {
        color: #0e3b57 !important;
        font-weight: 700 !important;
    }

    /* Table styling */
    .stDataFrameGlideDataEditor table {
        border-collapse: collapse;  
        width: 100%;
        border-radius: 8px;
        overflow: hidden;
        height: auto;
    }

    /* Zebra rows */
    .stDataFrameGlideDataEditor table tr:nth-child(even) {
        background-color: #f2f6fc !important;
    }

    /* Buttons */
    .stFormSubmitButton>button {
        background-color: #2f66c7 !important;
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        transition: 0.3s;
        font-size: 16px;
        font-weight: 600;
    }

    .stFormSubmitButton>button:hover {
        background-color: #0e3b57 !important;
        transform: translateY(-1px);
    }
            
    .stButton>button {
        background-color: #2f66c7 !important;
        color: white !important;
        border: none !important;
        padding: 6px 20px !important;
        border-radius: 6px !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        transition: 0.2s;
    }

    .stButton>button:hover {
        background-color: #0e3b57 !important;
        transform: translateY(-1px);
    }

    /* Form labels */
    .css-1p3nkdb, label {
        font-weight: 800 !important;
        color: #2b3e50 !important;
    }

    /* Select box styling */
    .css-1wy0on6, .stSelectbox {
        background-color: white !important;
        color: #2b3e50 !important;
    }

    </style>
""", unsafe_allow_html=True)



st.title("👨‍💼 Employee Management Dashboard")


# -------------------------
# Column Layout
# -------------------------
col1, col2 = st.columns(2)

# -------------------------
# Form: Add New Employee
# -------------------------
with col1:
    st.header("➕ Add New Employee")

    with st.form("add_employee_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        salary = st.number_input("Salary", min_value=0.0, step=100.0)

        submit_button = st.form_submit_button("Add Employee")

    if submit_button:
        # Validation checks
        if not name.strip():
            st.error("❌ Name cannot be empty.")
        elif age <= 0:
            st.error("❌ Age must be greater than 0.")
        elif salary <= 0:
            st.error("❌ Salary must be greater than 0.")
        else:
            response, code = api_add_employee(name, age, salary)
            if code == 200:
                st.success(f"✅ Employee added successfully with ID: {response.get('employee_id')}")
            else:
                st.error(f"❌ Error ({code}): {response}")

# -------------------------
# Table: View All Employees
# -------------------------
with col2:
    st.header("📋 Employee List")

    employees, code = api_get_employees()

    if code == 200 and isinstance(employees, list):
        df = pd.DataFrame(employees)
        df = df.rename(columns={
            "employee_id": "Employee ID",
            "name": "Name",
            "age": "Age",
            "salary": "Salary"
        })
        df = df.astype(str)
        st.dataframe(df)
    else:
        st.error(f"Error loading employees: {employees}")


# -------------------------
# Delete Employee
# -------------------------
st.header("✖️ Delete Employee")

employees, _ = api_get_employees()
emp_ids = [emp["employee_id"] for emp in employees] if isinstance(employees, list) else []

selected_id = st.selectbox("Select Employee ID to Delete", emp_ids)

if st.button("Delete Employee"):
    response, code = api_delete_employee(selected_id)
    if code == 200:
        st.success(f"Deleted Employee with ID: {selected_id}")
    else:
        st.error(f"Error ({code}): {response}")


# -------------------------
# Stats: Median Values
# -------------------------
st.header("📊 Statistics")

median_age, median_salary = api_get_stats()

colA, colB = st.columns(2)

with colA:
    st.metric(label="Median Age", value=median_age if median_age is not None else "N/A")

with colB:
    st.metric(label="Median Salary", value=median_salary if median_salary is not None else "N/A")

