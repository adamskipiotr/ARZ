import sqlite3
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)

DATABASE = 'database.db'
conn = sqlite3.connect(DATABASE)
conn.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, ''username TEXT, password TEXT, role TEXT)')
conn.close()
cors = CORS()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    from .images import images
    from .auth import auth

    app.register_blueprint(images, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    cors.init_app(app)

    return app
