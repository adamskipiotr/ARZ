from flask import Flask
from os import path
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .images import images

    app.register_blueprint(images, url_prefix='/')


    #
    # login_manager = LoginManager()
    # login_manager.login_view = 'auth.login'
    # login_manager.init_app(app)
    #
    # @login_manager.user_loader
    # def load_user(id):
    #     return User.query.get(int(id))
    #
    return app


# def create_database(app):
#     if not path.exists('website/' + DB_NAME):
#         db.create_all(app=app)
#         print('Created Database!')