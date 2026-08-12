from flask_sqlalchemy import SQLAlchemy


# Create SQLAlchemy object
db = SQLAlchemy()


class Student(db.Model):

    # Primary key
    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Student name
    name = db.Column(
        db.String(100),
        nullable=False
    )

    # Department
    department = db.Column(
        db.String(50),
        nullable=False
    )

    # Age
    age = db.Column(
        db.Integer,
        nullable=False
    )

    # Marks
    marks = db.Column(
        db.Float,
        nullable=False
    )

    # Attendance percentage
    attendance = db.Column(
        db.Float,
        nullable=False
    )

    # Convert SQLAlchemy object into dictionary
    # This is useful for REST API responses
    def to_dict(self):

        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "age": self.age,
            "marks": self.marks,
            "attendance": self.attendance
        }

    def __repr__(self):

        return (
            f"Student("
            f"{self.id}, "
            f"{self.name}, "
            f"{self.department}, "
            f"{self.marks})"
        )