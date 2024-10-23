from __init__ import db  # Import the SQLAlchemy instance from the initialization file
from flask_login import UserMixin  # Import UserMixin to add methods required by Flask-Login
from sqlalchemy.sql import func  # Import func to use database functions like getting the current time

# Define the User model, inheriting from db.Model and UserMixin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the user
    email = db.Column(db.String(150), unique=True)  # Unique email for the user, limited to 150 characters
    password = db.Column(db.String(150))  # User's password (hashed), limited to 150 characters
    first_name = db.Column(db.String(150))  # User's first name, limited to 150 characters
    workouts = db.relationship('Workout')  # One-to-many relationship with the Workout model
    goals = db.relationship('Goal')  # One-to-many relationship with the Goal model

# Define the Workout model, representing a user's workout session
class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the workout
    activity = db.Column(db.String(150))  # Name or type of activity, limited to 150 characters
    duration = db.Column(db.Integer)  # Duration of the workout in minutes
    date = db.Column(db.DateTime(timezone=True), default=func.now())  # Date and time of the workout, default to current time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking the workout to the user

# Define the Goal model, representing a fitness goal set by the user
class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key for the goal
    description = db.Column(db.String(1000))  # Detailed description of the goal, up to 1000 characters
    target = db.Column(db.Integer)  # Target duration in minutes to achieve for the goal
    progress = db.Column(db.Integer, default=0)  # Current progress towards the goal, defaults to 0
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key linking the goal to the user
