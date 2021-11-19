import json
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask import Blueprint, request
import sqlite3

DATABASE = 'database.db'
auth = Blueprint('auth', __name__)
authorize = HTTPBasicAuth()


@auth.route('/login', methods=['POST'])
def login():
    content = request.json
    username = content['username']
    password = content['password']
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(f"SELECT user_id FROM users WHERE username='{username}' AND password='{password}'")
    user = cur.fetchall()
    con.close()
    if len(user) > 0:
        print('Logowanie zakonczone sukcesem')
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'},
    else:
        print('Logowanie nieudane')
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
#@authorize.verify_password


@authorize.login_required
@auth.route('/response',methods=['GET'])
def get_response():
    return jsonify('You are an authenticate person to see this message')

@auth.route('/signup', methods=['POST'])
def signUp():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']
    con = sqlite3.connect(DATABASE)
    cur = con.cursor()
    cur.execute(f"INSERT INTO users (username, password) VALUES('{username}','{password}')")
    con.commit()
    con.close()
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
