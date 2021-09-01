from flask import Blueprint, render_template
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
@login_required
def index():
    return render_template('index.html')


@main.route('/about')
@login_required
def about():
    return render_template('about.html')


@main.route('/inventory')
@login_required
def inventory():
    return render_template('inventory.html')
