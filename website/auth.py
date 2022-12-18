from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash # Library for password hashing
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

# Handles methods used on login endpoint.
@auth.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user.is_authenticated)
    # Redirect user to home page if already signed in.
    if current_user.is_authenticated:
        return redirect(url_for('routes.home'))

    # Post request handle signing up and logging in. 
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        # If the user already exists in the database
        # And if the password matches the password in the database, we log in the user.
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('routes.home'))
                
            # If the password is incorrect, notify the user.
            else:
                flash('Incorrect password, try again.', category='error')

        # If the user does not exists in the database, create a new one.
        else:
            new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('routes.home'))

    return render_template("login.html", user=current_user)

# The logout endpoint only handles post requests.
# We logout the user and then navigate the user to the login page.
@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


