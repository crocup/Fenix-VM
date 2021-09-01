from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return {"1": "2"}


@main.route('/inventory')
def inventory():
    return {"1": "2"}
