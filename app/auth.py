"""
Авторизация и создание нового пользователя в приложении
Dmitry Livanov, 2020
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db, logger, db_login
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('newlogin.html')


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    logger.info("Logout")
    result_json = {
        "time": datetime.now(),
        "task": "logout",
        "message": f"Logout"
    }
    posts = db_login["logins"]
    posts.insert(result_json)
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    user = User.query.filter_by(
        email=email).first()  # if this returns a user, then the email already exists in database
    if user:  # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    logger.info(f"Create new user: {name}")
    result_json = {
        "time": datetime.now(),
        "task": "create",
        "message": f"Create new user: {name}"
    }
    posts = db_login["logins"]
    posts.insert(result_json)
    return redirect(url_for('auth.login'))


@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        logger.warning(f"Login or password incorrect")
        return redirect(url_for('auth.login'))  # if user doesn't exist or password is wrong, reload the page
    login_user(user, remember=remember)
    logger.info(f"Success login: {user.name}")
    result_json = {
        "time": datetime.now(),
        "task": "login",
        "message": f"Success login: {user.name}"
    }
    posts = db_login["logins"]
    posts.insert(result_json)
    return redirect(url_for('main.dashboard'))
