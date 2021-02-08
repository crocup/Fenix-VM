import atexit
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from datetime import datetime
from flask_uuid import FlaskUUID
import logging.config
import json
import sentry_sdk
from pymongo import MongoClient
from sentry_sdk.integrations.flask import FlaskIntegration
from apscheduler.schedulers.background import BackgroundScheduler
from .config import SENTRY_DSN

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[FlaskIntegration()]
)

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
with open("logging.json", 'r') as logging_configuration_file:
    config_dict = json.load(logging_configuration_file)

logging.config.dictConfig(config_dict)
logger = logging.getLogger(__name__)
client_mongo = MongoClient()
db_scanner = client_mongo['scanner']
db_login = client_mongo['login']

from .models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


def time():
    now = datetime.now()  # current date and time
    date_time = now.strftime("%d.%m.%Y %H:%M:%S")
    return date_time


# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from app import models
from app import main

from .scheduler import scheduler_host_discovery, scheduler_scanner
scheduler = BackgroundScheduler()
scheduler.add_job(func=scheduler_host_discovery, trigger="interval",  minutes=5)
scheduler.add_job(func=scheduler_scanner, trigger="interval",  hours=24)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
