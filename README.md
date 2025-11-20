# asg-tracker
# ASG IT Flask App

A complete Employee/Employer Management Portal with:
- Employee registration and login (see current job openings)
- Employer login (see consultant list after login)
- Rich UI with ASG IT banner, centered design, modern forms

---

## Features
- **Employee Registration** (`/register`) – New employees can sign up.
- **Login** (`/login`) – Employees and Employers log in.
    - Employees are redirected to their dashboard to view job openings (`/employee_dashboard`).
    - Employers are redirected to their dashboard with the consultant list (`/employer_dashboard`).
- **Session Management** – Secure login system using Flask sessions.
- **MongoDB** for data storage (users, consultants, job openings).
- **Styled, professional UI** for all pages.

---

## Setup Instructions

### Prerequisites
- Python 3.7+
- MongoDB running locally (`mongodb://localhost:27017/`)

---

### 1. **MongoDB installation steps**

#### **Ubuntu / Debian**
```sh
# Import public key
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

# Create a MongoDB list file
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

# Update the packages and install MongoDB
sudo apt-get update
sudo apt-get install -y mongodb-org

# Start MongoDB Service
sudo systemctl start mongod
sudo systemctl enable mongod

# Check status
sudo systemctl status mongod
```

#### **CentOS / RHEL**
```sh
cat <<EOF | sudo tee /etc/yum.repos.d/mongodb-org-6.0.repo
[mongodb-org-6.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/centos/7/mongodb-org/6.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://www.mongodb.org/static/pgp/server-6.0.asc
EOF

sudo yum install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

#### **Windows**
- Download the installer: [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- Run installer and follow steps in wizard.
- After install, use the Services window to start MongoDB (or use `mongod` command in terminal).

#### **Check MongoDB is running**
```sh
mongo --eval 'db.runCommand({ connectionStatus: 1 })'
```

---

### 2. **Clone repository**

```sh
git clone https://github.com/madhuchilipi/asg-tracker.git
cd asg-tracker
```

### 3. **Install dependencies**
```sh
pip install Flask pymongo
```
> If using requirements.txt, run `pip install -r requirements.txt`

### 4. **Run the app**
```sh
python3 app.py
```

Or with Flask CLI:
```sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

### 5. **Access the app**
- Open your browser and navigate to:  
  `http://localhost:5000`  
  or  
  `http://<your-local-ip>:5000`

---

## Sample Logins

### Employees (view job openings):
- Email: alice@asg.com Password: pass123
- Email: bob@asg.com Password: pass456

### Employer (view consultant list):
- Email: employer@asg.com Password: admin

---

## Pages and Functionality

**Employee Registration**
- Go to `/register` to sign up.
- Required fields: name, email, password, designation, consultant name.
- On success: you can log in as employee.

**Login**
- Go to `/login`, select your role ("employee" or "employer"), enter email/password.
- Redirects based on role.

**Employee Dashboard (`/employee_dashboard`)**
- Shows current job openings with title, description, location.

**Employer Dashboard (`/employer_dashboard`)**
- Shows a table of consultants with name, email, expertise.

**Logout**
- Click the "Logout" link on dashboard pages to end your session.

---

## Customizing

- To add/remove sample users, edit the seed section in `app.py`.
- To add new openings or consultants, insert records in MongoDB `openings`/`consultants` collections.
- For real password security, replace plaintext with `werkzeug.security.generate_password_hash()` and `check_password_hash()`.

---

## Troubleshooting

- **MongoDB Connection:** Make sure MongoDB is running and accessible.
- **Port/Firewall issues:** Use `host='0.0.0.0'` in `app.py` for network access.
- **Dependencies:** Install with pip as above if you see `ModuleNotFoundError`.

---

## File Structure

```
asg-tracker/
|-- app.py
|-- templates/
|     |-- register.html
|     |-- login.html
|     |-- employee_dashboard.html
|     |-- employer_dashboard.html
|-- README.md
```

---

## Contributing
Fork the repository and submit pull requests for features/fixes.

---

## License
MIT (or your preferred license)