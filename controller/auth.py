import json
from flask_httpauth import HTTPBasicAuth
from flask import jsonify
from flask import Blueprint, request

from service.user_service import UserService

DATABASE = 'database.db'
auth = Blueprint('auth', __name__)
authorize = HTTPBasicAuth()

user_service = UserService()



@authorize.verify_password
def verify_password(username, password):
    user = user_service.login(username, password)
    if len(user) > 0:
        return True
    return False

@auth.route('/response',methods=['GET'])
@authorize.login_required
def get_response():
    return jsonify('You are an authenticate person to see this message')

@auth.route('/signup', methods=['POST'])
def sign_up():
    request_data = request.get_json()
    user_service.save(request_data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@auth.route('/delete', methods=['DELETE'])
def delete_user():
    request_data = request.get_json()
    user_service.delete(request_data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}

@auth.route('/change-password', methods=['DELETE'])
def delete_user():
    request_data = request.get_json()
    user_service.change_password(request_data)
    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}
