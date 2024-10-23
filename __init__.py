from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Initialize the SQLAlchemy and LoginManager instances
db = SQLAlchemy()
login_manager = LoginManager()

# Factory function to create and configure the Flask app
def create_app():
    app = Flask(__name__)

    # Set the secret key for session management and security
    app.config.from_pyfile('config.py')


    # Configure the SQLite database URI for SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fitness.db'

    # Initialize the SQLAlchemy instance with the Flask app
    db.init_app(app)

    # Import and register the blueprints for views and authentication
    from views import views
    from auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Import models and create database tables if they don't exist
    from models import User, Workout, Goal
    with app.app_context():
        db.create_all()  # Create the database tables

    # Configure Flask-Login for user session management
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login route for unauthenticated users
    login_manager.init_app(app)  # Attach LoginManager to the app

    # Define the user loader callback function to load the user from the database
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))  # Query the User model to get the user by ID

    return app  # Return the configured Flask app instance
