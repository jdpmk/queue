from datetime import date, datetime, timedelta
from flask import Flask
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

class Course(db.Model):
    course_id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.String(100), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)

    def __repr__(self):
        return "<Course %r>" % self.course_id

class Assignment(db.Model):
    assignment_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    start_on = db.Column(db.DateTime(timezone=True), nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    frequency_metadata = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("course.course_id"), nullable=False)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/assignment/<int:assignment_id>")
def user_assignments(assignment_id):
    return get_upcoming_tasks(assignment_id)

class Frequency:
    DAILY = 0
    WEEKLY = 1

def get_upcoming_tasks(assignment_id):
    assignment = Assignment.query.filter_by(assignment_id=assignment_id).first()

    if assignment.frequency == Frequency.DAILY:
        # TODO: add metadata option to exclude weekends
        today = date.today()
        tomorrow = date.today() + timedelta(days=1)
        return [today, tomorrow]
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
            if occurs[day.weekday()]:
                this_week.append(day)
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

        return [this_week, next_week]
