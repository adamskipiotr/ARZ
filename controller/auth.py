import json
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask import Blueprint, request

from service.user_service import UserService

DATABASE = 'database.db'
auth = Blueprint('auth', __name__)
authorize = HTTPBasicAuth()

user_service = UserService()

@auth.route('/login', methods=['POST'])
def login():
    login_request_data = request.json
    user = user_service.login(login_request_data)
    if len(user) > 0:
        return json.dumps({'success': True}), 200, {'ContentType': 'application/json'},
    else:
        return json.dumps({'success': False}), 403, {'ContentType': 'application/json'}
#@authorize.verify_password


@authorize.login_required
@auth.route('/response',methods=['GET'])
def get_response():
    return jsonify('You are an authenticate person to see this message')

@auth.route('/signup', methods=['POST'])
def sign_up():
    request_data = request.get_json()
    user_service.save(request_data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
