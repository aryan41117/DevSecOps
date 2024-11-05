from auth import get_db

from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id, email, password, first_name):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name

    @staticmethod
    def get_user_by_email(email):
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE email = ?", (email,)).fetchone()
        return User(user['id'], user['email'], user['password'], user['first_name']) if user else None

class Workout:
    @staticmethod
    def create(activity, duration, user_id):
        db = get_db()
        db.execute("INSERT INTO workout (activity, duration, user_id) VALUES (?, ?, ?)", 
                   (activity, duration, user_id))
        db.commit()

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        return db.execute("SELECT * FROM workout WHERE user_id = ?", (user_id,)).fetchall()

class Goal:
    @staticmethod
    def create(description, target, user_id):
        db = get_db()
        db.execute("INSERT INTO goal (description, target, user_id) VALUES (?, ?, ?)", 
                   (description, target, user_id))
        db.commit()

    @staticmethod
    def get_all_by_user(user_id):
        db = get_db()
        return db.execute("SELECT * FROM goal WHERE user_id = ?", (user_id,)).fetchall()
