from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient("mongodb://192.168.1.231:27017/")
db = client["employee_db"]
collection = db["employees"]

@app.route("/", methods=["GET"])
def index():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    name = request.form.get("name")
    email = request.form.get("email")
    designation = request.form.get("designation")
    consultant = request.form.get("consultant")
    employee = {
        "name": name,
        "email": email,
        "designation": designation,
        "consultant": consultant
    }
    collection.insert_one(employee)
    return redirect(f"/employee/{email}")

@app.route("/employee/<email>", methods=["GET"])
def employee(email):
    employee = collection.find_one({"email": email})
    if not employee:
        return "Employee not found.", 404
    return render_template("employee.html", employee=employee)

@app.route("/employer", methods=["GET"])
def employer():
    employees = list(collection.find())
    return render_template("employer.html", employees=employees)

if __name__ == "__main__":
    app.run(debug=True)
