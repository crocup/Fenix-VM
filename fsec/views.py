# main.py
from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html', name=current_user.name)


@main.route('/about')
@login_required
def about():
    return render_template('about.html', name=current_user.name)
