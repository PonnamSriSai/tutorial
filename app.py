# created by PONNAM 
# 8 july 2025 21:56

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()

class Student(db.Model):
    __tablename__ = 'student' 

    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, nullable=False, unique=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)

class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, nullable=False, unique=True)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollment(db.Model):
    __tablename__ = 'enrollments'

    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')


@app.route("/", methods = ["GET", "POST"])
def index():
    return render_template("index.html", students = Student.query.all())

@app.route("/student/create", methods=["GET", "POST"])
def add_stud():
    try:
        if request.method == "POST":
        db.session.add(
            Student(
                roll_number = request.form['roll'],
                first_name = request.form['f_name'],
                last_name = request.form['l_name']
            )
        )
        db.session.commit()
        id = Student.query.filter_by(roll_number=request.form["roll"]).first().student_id
        course_code_map = {
            'course_1': 'CSE01',
            'course_2': 'CSE02',
            'course_3': 'CSE03',
            'course_4': 'BST13'
        }
        for course in request.form.getlist('courses'):
            actual_code = course_code_map.get(course)
            if actual_code:
                course = Course.query.filter_by(course_code=actual_code).first()
                if course:
                    enrollment = Enrollment(
                        estudent_id=id,
                        ecourse_id=course.course_id
                    )
                    db.session.add(enrollment)

                    db.session.commit()

        return redirect(url_for('index'))

    except SQLAlchemy.exc.IntegrityError:
        return render_template("""<p>Student already exists.please use different roll number!</p>""")
    else:
        eturn render_template("add_stud.html")

if __name__ == "__main__":
    app.run()