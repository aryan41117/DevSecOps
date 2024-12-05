from flask import Flask, g
from flask_login import LoginManager
import sqlite3
from flask_wtf import CSRFProtect
from models import create_tables, query_user_by_id

DATABASE = 'fitness.db'

csrf = CSRFProtect()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def create_app():
    app = Flask(__name__)
    # Set the secret key for session management and security
    app.config.from_pyfile('config.py')
    csrf.init_app(app)

    from auth import auth
    from views import views

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')

    # Initialize the database and create tables if they don’t exist
    with app.app_context():
        create_tables()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return query_user_by_id(user_id)

    # Close the database connection after each request
    @app.teardown_appcontext
    def close_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    return app
