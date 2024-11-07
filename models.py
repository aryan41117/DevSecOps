from flask_login import UserMixin
import sqlite3

DATABASE = 'fitness.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # To return rows as dictionaries
    return conn

def create_tables():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    first_name TEXT NOT NULL,
                    password TEXT NOT NULL
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Workout (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    activity TEXT NOT NULL,
                    duration INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS Goal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    description TEXT,
                    target INTEGER,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )''')
    conn.commit()
    conn.close()

class User(UserMixin):
    def __init__(self, id, email, first_name, password):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.password = password
        

    @classmethod
    def get(cls, user_id):
        db = get_db()
        user_data = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
        if user_data:
            return cls(user_data['id'], user_data['email'], user_data['first_name'], user_data['password'])
        return None

def query_user_by_id(user_id):
    return User.get(user_id)
