import json
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from flask_uuid import FlaskUUID


app = Flask(__name__)
app.debug = True
app.secret_key = 'hellos'
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)
Migrate(app, db)
FlaskUUID(app)
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


def time():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time


def get_config():
    with open('app/config.json', 'r') as f:
        config_json = json.load(f)
    return config_json


# blueprint for auth routes in our app
from .auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint

app.register_blueprint(main_blueprint)

# from .api import api as api_blueprint
#
# app.register_blueprint(api_blueprint)

from app import models
from app import main
