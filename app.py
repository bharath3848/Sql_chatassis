import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to connect to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('company.db')
    conn.row_factory = sqlite3.Row  # So we can access columns by name
    return conn

# Function to fetch employees by department
def get_employees_by_department(department):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Employees WHERE Department = ?"
    cursor.execute(query, (department,))
    employees = cursor.fetchall()
    conn.close()
    return employees

# Function to fetch the manager of a department
def get_manager_of_department(department):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT Manager FROM Departments WHERE Name = ?"
    cursor.execute(query, (department,))
    manager = cursor.fetchone()
    conn.close()
    return manager

# Function to fetch employees hired after a specific date
def get_employees_hired_after(date):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM Employees WHERE Hire_Date > ?"
    cursor.execute(query, (date,))
    employees = cursor.fetchall()
    conn.close()
    return employees

# Function to get the total salary expense of a department
def get_total_salary_expense(department):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT SUM(Salary) FROM Employees WHERE Department = ?"
    cursor.execute(query, (department,))
    total_salary = cursor.fetchone()[0]
    conn.close()
    return total_salary

@app.route("/ask", methods=["GET"])
def ask():
    query = request.args.get('query')
    response = {"answer": ""}
    
    if query is None:
        response["answer"] = "Please provide a query."
        return jsonify(response)

    # Query for employees in a department
    if "employees in the" in query.lower() and "department" in query.lower():
        department = query.split("in the")[1].strip().replace("department", "").strip()
        employees = get_employees_by_department(department)
        if employees:
            response["answer"] = [{"ID": emp["ID"], "Name": emp["Name"], "Department": emp["Department"], "Salary": emp["Salary"], "Hire_Date": emp["Hire_Date"]} for emp in employees]
        else:
            response["answer"] = "No employees found in this department."

    # Query for the manager of a department
    elif "manager of the" in query.lower() and "department" in query.lower():
        department = query.split("of the")[1].strip().replace("department", "").strip()
        manager = get_manager_of_department(department)
        if manager:
            response["answer"] = manager["Manager"]
        else:
            response["answer"] = "No manager found for this department."

    # Query for the total salary expense for a department
    elif "total salary expense for the" in query.lower():
        department = query.split("for the")[1].strip().replace("department", "").strip()
        total_salary = get_total_salary_expense(department)
        if total_salary is not None:
            response["answer"] = f"The total salary expense for {department} is ${total_salary}."
        else:
            response["answer"] = "No data found for this department."

    # Query for employees hired after a specific date
    elif "hired after" in query.lower():
        date = query.split("after")[1].strip()
        employees = get_employees_hired_after(date)
        if employees:
            response["answer"] = [{"ID": emp["ID"], "Name": emp["Name"], "Department": emp["Department"], "Salary": emp["Salary"], "Hire_Date": emp["Hire_Date"]} for emp in employees]
        else:
            response["answer"] = "No employees hired after this date."

    else:
        response["answer"] = "Sorry, I didn't understand your query."

    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
