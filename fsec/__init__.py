import os
from flask import Flask
# https://pythonru.com/uroki/19-struktura-i-jeskiz-prilozhenija-flask
# создание экземпляра приложения
fsec = Flask(__name__)
# fsec.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')



# import views
from . import views