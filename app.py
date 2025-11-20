from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
import os

app = Flask(__name__)
app.secret_key = os.environ.get('ASG_SECRET_KEY', 'asg_default_secret')

client = MongoClient("mongodb://localhost:27017/")
db = client["asg_db"]
users = db["users"]
openings = db["openings"]

def seed_data():
    if users.count_documents({"role": "employee"}) == 0:
        users.insert_many([
            {"email": "alice@asg.com", "password": "pass123", "name": "Alice", "designation": "Developer", "consultant": "Consultant A", "role": "employee"},
            {"email": "bob@asg.com", "password": "pass456", "name": "Bob", "designation": "Tester", "consultant": "Consultant B", "role": "employee"}
        ])
    if users.count_documents({"role": "employer"}) == 0:
        users.insert_one({"email": "employer@asg.com", "password": "admin", "name": "ASG Manager", "role": "employer"})
    if openings.count_documents({}) == 0:
        openings.insert_many([
            {"title": "ML Engineer", "location": "Bangalore", "years_of_exp": "2", "description": "Work on ASG's AI projects."},
            {"title": "Cloud Architect", "location": "Remote", "years_of_exp": "5", "description": "Cloud migration role."}
        ])
seed_data()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        designation = request.form['designation']
        consultant = request.form['consultant']
        if users.find_one({"email": email, "role": "employee"}):
            message = "Employee already registered."
        else:
            users.insert_one({
                "name": name, "email": email, "password": password,
                "designation": designation, "consultant": consultant, "role": "employee"
            })
            message = "Registration successful! Please login."
            return redirect('/login')
    return render_template('register.html', message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        role = request.form['role']
        email = request.form['email']
        password = request.form['password']
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

@app.route('/employee_dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect('/login')
    open_roles = list(openings.find({}))
    return render_template('employee_dashboard.html', openings=open_roles, name=session.get('name', ''))

@app.route('/employer_dashboard')
def employer_dashboard():
    if session.get('role') != 'employer':
        return redirect('/login')
    employees = list(users.find({'role': 'employee'}))
    return render_template('employer_dashboard.html', employees=employees)

@app.route('/add_requirement', methods=['POST'])
def add_requirement():
    if session.get('role') != 'employer':
        return redirect('/login')
    title = request.form['title']
    location = request.form['location']
    years_of_exp = request.form['years_of_exp']
    description = request.form['description']
    openings.insert_one({
        "title": title,
        "location": location,
        "years_of_exp": years_of_exp,
        "description": description
    })
    return redirect('/employer_dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)