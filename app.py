from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Configure MongoDB client
client = MongoClient("mongodb://localhost:27017/")
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
    # Data validation can be added here
    employee = {
        "name": name,
        "email": email,
        "designation": designation,
        "consultant": consultant
    }
    collection.insert_one(employee)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)