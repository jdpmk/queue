from datetime import date, datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from impl import *

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
