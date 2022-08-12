from datetime import date, datetime, timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self):
        return "<Course %r>" % self.course_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    start_on = db.Column(db.DateTime(timezone=True), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    frequency_metadata = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

    def __repr__(self):
        return "<Assignment %r>" % self.assignment_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def user(user_id):
    if request.method == "GET":
        user = User.query.filter_by(user_id=user_id).first()
        return user.as_dict()
    else:
        assert request.method == "POST"

        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        email = request.json["email"]

        user = User(first_name=first_name, last_name=last_name, email=email)
        db.session.add(user)
        db.session.commit()

@app.route("/course/<int:course_id>", methods=["GET", "POST"])
def course(course_id):
    if request.method == "GET":
        course = Course.query.filter_by(course_id=course_id).first()
        return course.as_dict()
    else:
        assert request.method == "POST"

        department = request.json["department"]
        number = request.json["number"]
        name = request.json["name"]
        user_id = request.json["user_id"]

        course = Course(department=department, number=number, name=name, user_id=user_id)
        db.session.add(course)
        db.session.commit()

@app.route("/assignment/<int:assignment_id>", methods=["GET", "POST"])
def assignment(assignment_id):
    if request.method == "GET":
        assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()
        return assignment.as_dict()
    else:
        assert request.method == "POST"

        name = request.json["name"]
        description = request.json.get("description", None)
        start_on = request.json["start_on"]
        frequency = request.json["frequency"]
        frequency_metadata = request.json.get("frequency_metadata", None)
        course_id = request.json["course_id"]

        assignment = Assignment(name=name,
                                description=description,
                                start_on=start_on,
                                frequency=frequency,
                                frequency_metadata=frequency_metadata,
                                course_id=course_id)
        db.session.add(assignment)
        db.session.commit()

@app.route("/user/<int:user_id>/courses", methods=["GET"])
def user_courses(user_id):
    assert request.method == "GET"
    courses = Course.query.filter_by(user_id=user_id)
    return [course.as_dict() for course in courses]

@app.route("/course/<int:course_id>/assignments", methods=["GET"])
def course_assignments(course_id):
    assert request.method == "GET"
    assignments = Assignment.query.filter_by(course_id=course_id)
    return [assignment.as_dict() for assignment in assignments]

@app.route("/assignment/<int:assignment_id>/upcoming", methods=["GET"])
def user_assignments(assignment_id):
    assert request.method == "GET"

    assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()

    if assignment.frequency == Frequency.DAILY:
        # TODO: add metadata option to exclude weekends
        today = date.today()
        tomorrow = today + timedelta(days=1)
        return { "today": today, "tomorrow": tomorrow }
    elif assignment.frequency == Frequency.WEEKLY:
        U = (assignment.frequency_metadata >> 6) & 1
        M = (assignment.frequency_metadata >> 5) & 1
        T = (assignment.frequency_metadata >> 4) & 1
        W = (assignment.frequency_metadata >> 3) & 1
        H = (assignment.frequency_metadata >> 2) & 1
        F = (assignment.frequency_metadata >> 1) & 1
        S = (assignment.frequency_metadata >> 0) & 1

        # aligned with weekday() (0 = M, 1 = T, etc.)
        occurs = [M, T, W, H, F, S, U]

        this_week = []
        next_week = []
        day = date.today()

        # aggregate all remaining days this week
        while True:
            if occurs[day.weekday()]: this_week.append(day)
            day += timedelta(days=1)
            if day.weekday() == 6:
                break

        # aggregate all days next week
        while True:
            if occurs[day.weekday()]:
                next_week.append(day)
            day += timedelta(days=1)
            if day.weekday() == 6:
                break

        return { "this_week": this_week, "next_week": next_week }

class Frequency:
    DAILY = 0
    WEEKLY = 1

def insert_test_data(db):
    def add(db, obj):
        db.session.add(obj)
        db.session.commit()

    joydeep = User(first_name="Joydeep", last_name="Mukherjee", email="joydeep2@illinois.edu")
    add(db, joydeep)

    cs374 = Course(department="CS", number=374, name="Algorithms", user_id=joydeep.user_id)
    add(db, cs374)

    cs421 = Course(department="CS", number=421, name="Compilers", user_id=joydeep.user_id)
    add(db, cs421)

    hw = Assignment(name="HW",
                    description="Daily homework",
                    start_on=date.today() + timedelta(days=-4),
                    frequency=Frequency.DAILY,
                    frequency_metadata=None,
                    course_id=cs374.course_id)
    mp = Assignment(name="MP",
                    description="Weekly project",
                    start_on=date.today(),
                    frequency=Frequency.WEEKLY,
                    frequency_metadata=65,  # 1 0 0 0 0 0 1
                    course_id=cs421.course_id)
    add(db, hw)
    add(db, mp)

db.create_all()
insert_test_data(db)
