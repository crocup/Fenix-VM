import os
from flask import Flask
from flask_cors import CORS
from rq import Queue
from worker import conn

q = Queue(name='fsec', connection=conn)


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
    CORS(app)
    from .views import main
    from fsec.modules.hostdiscovery.api import hostdiscovery
    app.register_blueprint(main)
    app.register_blueprint(hostdiscovery)
    return app
