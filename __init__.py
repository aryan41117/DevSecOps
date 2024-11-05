from flask import Flask
from flask_login import LoginManager
# Factory function to create and configure the Flask app
def create_app():
    app = Flask(__name__)

    # Set the secret key for session management and security
    app.config.from_pyfile('config.py')

    # Initialize LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
  
    # Import and register the blueprints for views and authentication
    from views import views
    from auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    return app
