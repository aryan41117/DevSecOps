from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from __init__ import db

# Create a Blueprint for authentication routes
auth = Blueprint('auth', __name__)

# Route for login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the user submits the login form
        email = request.form.get('email')  # Get the email from the form
        password = request.form.get('password')  # Get the password from the form
        
        # Query the user by email
        user = User.query.filter_by(email=email).first()
        
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password, password):
            login_user(user)  # Log the user in
            return redirect(url_for('views.home'))  # Redirect to the home page
        else:
            # Flash an error message if login fails
            flash('Login unsuccessful. Check email and password', category='error')

    # Render the login template, passing the current user
    return render_template("login.html", user=current_user)

# Route for logout
@auth.route('/logout')
def logout():
    logout_user()  # Log the user out
    return redirect(url_for('auth.login'))  # Redirect to the login page

# Route for sign-up (registration)
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':  # If the user submits the sign-up form
        email = request.form.get('email')  # Get the email from the form
        first_name = request.form.get('firstName')  # Get the first name from the form
        password1 = request.form.get('password1')  # Get the first password entry
        password2 = request.form.get('password2')  # Get the second password entry

        # Query the user by email to check if it already exists
        user = User.query.filter_by(email=email).first()
        
        # Perform validation checks
        if user:  # Check if the email already exists
            flash('Email already exists.', category='error')
        elif password1 != password2:  # Check if the passwords match
            flash('Passwords don’t match.', category='error')
        else:
            # Create a new user with a hashed password
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='pbkdf2:sha256'))
            db.session.add(new_user)  # Add the new user to the database
            db.session.commit()  # Commit the changes
            login_user(new_user)  # Log the new user in
            return redirect(url_for('views.home'))  # Redirect to the home page

    # Render the sign-up template, passing the current user
    return render_template("sign_up.html", user=current_user)
