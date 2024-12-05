from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db, User

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        db = get_db()
        user_data = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()

        if user_data:
            user = User(user_data['id'], user_data['email'], user_data['first_name'], user_data['password'])
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('views.home'))
        
        flash('Login unsuccessful. Check email and password', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        db = get_db()
        existing_user = db.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        
        if existing_user:
            flash('Email already exists.', category='error')
        elif password1 != password2:
            flash('Passwords don’t match.', category='error')
        else:
            hashed_password = generate_password_hash(password1, method='pbkdf2:sha256')
            db.execute('INSERT INTO users (email, first_name, password) VALUES (?, ?, ?)',
                       (email, first_name, hashed_password))
            db.commit()
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))  

