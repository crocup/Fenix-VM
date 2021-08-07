# import os
# from flask import Flask
#
# # https://pythonru.com/uroki/19-struktura-i-jeskiz-prilozhenija-flask
# # создание экземпляра приложения
# from flask_migrate import Migrate
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager

# app = Flask(__name__, static_folder="web/static", template_folder="web/templates")
# app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
#
# # инициализирует расширения
# db = SQLAlchemy(app)
# db.init_app(app)

# login_manager = LoginManager()
# login_manager.login_view = 'auth.login'
# login_manager.init_app(app)
#
# from .models import User
#
#
# @login_manager.user_loader
# def load_user(user_id):
#     # since the user_id is just the primary key of our user table, use it in the query for the user
#     return User.query.get(int(user_id))
#
#
# # blueprint for auth routes in our app
# from .auth import auth as auth_blueprint
#
# app.register_blueprint(auth_blueprint)
#
# # blueprint for non-auth parts of app
# from .views import main as main_blueprint
# app.register_blueprint(main_blueprint)


# init.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_folder="web/static", template_folder="web/templates")
    app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
