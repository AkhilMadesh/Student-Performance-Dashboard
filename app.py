from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database config
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# ---------------- MODEL ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

# ---------------- CREATE TABLES ----------------
with app.app_context():
    db.create_all()

# ---------------- ROUTES ----------------
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([
        {"name": s.name, "subject": s.subject, "marks": s.marks}
        for s in students
    ])

@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    student = Student(
        name=data["name"],
        subject=data["subject"],
        marks=data["marks"]
    )
    db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Student added"})

@app.route("/add_bulk", methods=["POST"])
def add_bulk():
    students = request.json
    for s in students:
        student = Student(
            name=s["name"],
            subject=s["subject"],
            marks=s["marks"]
        )
        db.session.add(student)
    db.session.commit()
    return jsonify({"message": "Bulk students added"})

# ---------------- RUN SERVER ----------------
if __name__ == "__main__":
    print("Starting Flask server...")
    app.run(debug=True)
