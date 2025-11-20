from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = os.environ.get('ASG_SECRET_KEY', 'asg_default_secret')

# Configure file upload
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

client = MongoClient("mongodb://localhost:27017/")
db = client["asg_db"]
users = db["users"]
openings = db["openings"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def seed_data():
    # Set both admin logins for employer and employee
    if users.count_documents({"role": "employee", "email": "admin"}) == 0:
        users.insert_one({
            "email": "admin",
            "password": "admin",
            "name": "Admin Emp",
            "designation": "Developer",
            "consultant": "Consultant A",
            "role": "employee"
        })
    if users.count_documents({"role": "employer", "email": "admin"}) == 0:
        users.insert_one({
            "email": "admin",
            "password": "admin",
            "name": "Admin Employer",
            "role": "employer"
        })
    if openings.count_documents({}) == 0:
        openings.insert_many([
            {"title": "ML Engineer", "location": "Bangalore", "years_of_exp": "2", "description": "Work on ASG's AI projects."},
            {"title": "Cloud Architect", "location": "Remote", "years_of_exp": "5", "description": "Cloud migration role."}
        ])
seed_data()

# --------------- Employee Module ---------------
@app.route('/register', methods=['GET', 'POST'])
def employee_register():
    message = None
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        designation = request.form['designation']
        consultant = request.form['consultant']
        skills_input = request.form.get('skills', '')
        
        # Process skills - split by comma and trim whitespace
        skills = [skill.strip() for skill in skills_input.split(',') if skill.strip()]
        
        # Handle resume file upload
        resume_file = request.files.get('resume')
        resume_path = None
        
        if resume_file and resume_file.filename:
            if allowed_file(resume_file.filename):
                # Create a unique filename using email
                filename = secure_filename(f"{email}_{resume_file.filename}")
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                resume_file.save(filepath)
                resume_path = filepath
            else:
                message = "Invalid file type. Please upload PDF or DOC files only."
                return render_template('register.html', message=message)
        
        if users.find_one({"email": email, "role": "employee"}):
            message = "Employee already registered."
        else:
            user_data = {
                "name": name, 
                "email": email, 
                "password": password,
                "designation": designation, 
                "consultant": consultant, 
                "skills": skills,
                "resume_path": resume_path,
                "role": "employee"
            }
            users.insert_one(user_data)
            message = "Registration successful! Please login."
            return redirect('/login')
    return render_template('register.html', message=message)

@app.route('/employee_dashboard')
def employee_dashboard():
    if session.get('role') != 'employee':
        return redirect('/login')
    open_roles = list(openings.find({}))
    return render_template('employee_dashboard.html', openings=open_roles, name=session.get('name', ''))

# --------------- Employer Module ---------------
@app.route('/employer_dashboard')
def employer_dashboard():
    if session.get('role') != 'employer':
        return redirect('/login')
    employees = list(users.find({'role': 'employee'}))
    return render_template('employer_dashboard.html', employees=employees)

# --------------- Requirements Module ---------------
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

# --------------- Common Routes ---------------
@app.route('/')
def home():
    return redirect('/login')

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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)