from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager, Command, Shell
from flask_login import LoginManager
import os, config
# https://pythonru.com/uroki/19-struktura-i-jeskiz-prilozhenija-flask
# создание экземпляра приложения
fsec = Flask(__name__)
fsec.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

# инициализирует расширения
manager = Manager(fsec)
db = SQLAlchemy(fsec)
migrate = Migrate(fsec,  db)
manager.add_command('db', MigrateCommand)

# import views
from . import views