from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    jsonify
)

from models import db, Student


# --------------------------------------------------
# Create Flask application
# --------------------------------------------------

app = Flask(__name__)


# --------------------------------------------------
# Database configuration
# --------------------------------------------------

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///../database/students.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Connect SQLAlchemy with Flask
db.init_app(app)


# --------------------------------------------------
# Create database and table
# --------------------------------------------------

with app.app_context():
    db.create_all()


# ==================================================
# HTML ROUTES
# ==================================================


# --------------------------------------------------
# Home page
# --------------------------------------------------

@app.route("/")
def home():

    return render_template("index.html")


# --------------------------------------------------
# Display all students
# --------------------------------------------------

@app.route("/students")
def students():

    students = Student.query.all()

    return render_template(
        "students.html",
        students=students
    )


# --------------------------------------------------
# Add student using HTML form
# --------------------------------------------------

@app.route(
    "/students/add",
    methods=["GET", "POST"]
)
def add_student():

    if request.method == "POST":

        # Get values from HTML form
        name = request.form["name"]
        department = request.form["department"]
        age = request.form["age"]
        marks = request.form["marks"]
        attendance = request.form["attendance"]

        # Create Student object
        student = Student(
            name=name,
            department=department,
            age=int(age),
            marks=float(marks),
            attendance=float(attendance)
        )

        # Add to database
        db.session.add(student)

        # Save changes
        db.session.commit()

        return redirect(url_for("students"))

    return render_template("add_student.html")


# --------------------------------------------------
# Delete student
# --------------------------------------------------

@app.route(
    "/students/delete/<int:id>",
    methods=["POST"]
)
def delete_student(id):

    student = db.session.get(Student, id)

    if student:

        db.session.delete(student)
        db.session.commit()

    return redirect(url_for("students"))


# ==================================================
# REST API
# ==================================================


# --------------------------------------------------
# GET all students
# --------------------------------------------------

@app.route(
    "/api/students",
    methods=["GET"]
)
def get_students_api():

    students = Student.query.all()

    return jsonify([
        student.to_dict()
        for student in students
    ])


# --------------------------------------------------
# GET one student
# --------------------------------------------------

@app.route(
    "/api/students/<int:id>",
    methods=["GET"]
)
def get_student_api(id):

    student = db.session.get(Student, id)

    if not student:

        return jsonify({
            "error": "Student not found"
        }), 404

    return jsonify(student.to_dict())


# --------------------------------------------------
# POST - Create student
# --------------------------------------------------

@app.route(
    "/api/students",
    methods=["POST"]
)
def create_student_api():

    data = request.get_json()

    # Validate JSON
    if not data:

        return jsonify({
            "error": "JSON data is required"
        }), 400

    # Check required fields
    required_fields = [
        "name",
        "department",
        "age",
        "marks",
        "attendance"
    ]

    for field in required_fields:

        if field not in data:

            return jsonify({
                "error": f"Missing field: {field}"
            }), 400

    # Create student
    student = Student(
        name=data["name"],
        department=data["department"],
        age=int(data["age"]),
        marks=float(data["marks"]),
        attendance=float(data["attendance"])
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": student.to_dict()
    }), 201


# --------------------------------------------------
# PUT - Update student
# --------------------------------------------------

@app.route(
    "/api/students/<int:id>",
    methods=["PUT"]
)
def update_student_api(id):

    student = db.session.get(Student, id)

    if not student:

        return jsonify({
            "error": "Student not found"
        }), 404

    data = request.get_json()

    if "name" in data:
        student.name = data["name"]

    if "department" in data:
        student.department = data["department"]

    if "age" in data:
        student.age = int(data["age"])

    if "marks" in data:
        student.marks = float(data["marks"])

    if "attendance" in data:
        student.attendance = float(data["attendance"])

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": student.to_dict()
    })


# --------------------------------------------------
# DELETE student
# --------------------------------------------------

@app.route(
    "/api/students/<int:id>",
    methods=["DELETE"]
)
def delete_student_api(id):

    student = db.session.get(Student, id)

    if not student:

        return jsonify({
            "error": "Student not found"
        }), 404

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    })


# ==================================================
# RUN APPLICATION
# ==================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )