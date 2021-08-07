import os
from flask import Flask

# https://pythonru.com/uroki/19-struktura-i-jeskiz-prilozhenija-flask
# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')

from . import views