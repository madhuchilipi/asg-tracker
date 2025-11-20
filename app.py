from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.environ.get('ASG_SECRET_KEY', 'asg_default_secret')  # For sessions

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["asg_db"]
users = db["users"]
consultants = db["consultants"]
openings = db["openings"]

# ---- Seed demo data if empty (for demo/testing) ----
def seed_data():
    # Employees
    if users.count_documents({"role": "employee"}) == 0:
        users.insert_many([
            {"email": "alice@asg.com", "password": "pass123", "name": "Alice", "role": "employee"},
            {"email": "bob@asg.com", "password": "pass456", "name": "Bob", "role": "employee"}
        ])
    # Employers
    if users.count_documents({"role": "employer"}) == 0:
        users.insert_many([
            {"email": "employer@asg.com", "password": "admin", "name": "ASG Manager", "role": "employer"}
        ])
    # Consultants
    if consultants.count_documents({}) == 0:
        consultants.insert_many([
            {"name": "Consultant A", "email": "c.a@asg.com", "expertise": "Cloud"},
            {"name": "Consultant B", "email": "c.b@asg.com", "expertise": "AI & ML"},
            {"name": "Consultant C", "email": "c.c@asg.com", "expertise": "DevOps"}
        ])
    # Openings
    if openings.count_documents({}) == 0:
        openings.insert_many([
            {"title": "ML Engineer", "description": "Work on ASG's AI projects.", "location": "Bangalore"},
            {"title": "Cloud Architect", "description": "Cloud migration role.", "location": "Remote"},
            {"title": "Frontend Developer", "description": "React experience required.", "location": "Hyderabad"}
        ])
seed_data()

@app.route('/')
def home():
    return redirect('/login')

# --- Login Page ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        role = request.form.get('role')
        email = request.form.get('email')
        password = request.form.get('password')
        user = users.find_one({"email": email, "role": role})
        if user and user['password'] == password:
            session['email'] = user['email']
            session['role'] = user['role']
            session['name'] = user.get('name', user['email'])
            if role == 'employee':
                return redirect('/employee_dashboard')
            elif role == 'employer':
                return redirect('/employer_dashboard')
        else:
            error = "Invalid credentials"
    return render_template('login.html', error=error)

# --- Employee Dashboard: Show current openings ---
@app.route('/employee_dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect('/login')
    open_roles = list(openings.find({}))
    return render_template('employee_dashboard.html', openings=open_roles, name=session.get('name', ''))

# --- Employer Dashboard: Show consultant list ---
@app.route('/employer_dashboard')
def employer_dashboard():
    if session.get('role') != 'employer':
        return redirect('/login')
    c_list = list(consultants.find({}))
    return render_template('employer_dashboard.html', consultants=c_list, name=session.get('name', ''))

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)