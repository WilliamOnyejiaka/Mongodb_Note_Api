from flask import Blueprint, request, jsonify
from src.api.v1.models.User import User
import validators
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post("/sign_up")
def sign_up():
    name = request.get_json().get('name', None)
    email = request.get_json().get('email', None)
    password = request.get_json().get('password', None)

    if name == None:
        return jsonify({'error': True, 'message': "name is missing"}), 400
    if len(name) < 2:
        return jsonify({'error': True, 'message': "name length should be greater than 1"}), 400 
    if password == None:
        return jsonify({'error': True, 'message': "password is missing"}), 400
    if len(password) < 5:
        return jsonify({'error': True, 'message': "password length must be greater than 4"}), 400
    if email == None:
        return jsonify({'error': True, 'message': "email is missing"}), 400
    if not validators.email(email):
        return jsonify({'error': True, 'message': "email is not valid"}), 400
    if User.get_user(email, ['email']):
        return jsonify({'error': True, 'message': "email already exits"}), 400

    user = User.create_user(name, email, password)
    if user:
        return jsonify({'error': False, 'message': "user created"}), 200
    return jsonify({'error': True, 'message': "user not created"}), 500


@auth.get("/login")
def login():
    email = request.authorization.get('username', None)
    password = request.authorization.get('password', None)

    if not email:
        return jsonify({'error': True, 'message': "email required"}), 400
    if User.get_user(email, ['email']):
        user_attr = User.get_user(email)
        valid_password = check_password_hash(user_attr['password'], password)
        if valid_password:
            access_token = create_access_token(identity=user_attr['_id'])
            refresh_token = create_refresh_token(identity=user_attr['_id'])
            return jsonify({
                'error': False,
                'user_data': {
                   'id':user_attr['_id'],
                   'email':user_attr['email'],
                   'name':user_attr['name'],
                   'created_at': user_attr['created_at'],
                   'updated_at': user_attr['updated_at'],
                },
                'tokens': {
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }), 200
        return jsonify({'error': True, 'message': "invalid credientials"}), 400

    return jsonify({'error': True, 'message': "invalid credientials"}), 400


@auth.get("/token/refresh")
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify({'access_token':access_token}),200

@auth.patch("/update_email")
@jwt_required()
def update_email():
    user_id = get_jwt_identity()
    email = request.get_json().get('email',None)

    if email == None:
        return jsonify({'error': True, 'message': "email is missing"}), 400
    if not validators.email(email):
        return jsonify({'error': True, 'message': "email is not valid"}), 400
    if User.get_user(email, ['email']):
        return jsonify({'error': True, 'message': "email already exits"}), 400
    
    updated = User.update_email(user_id,email)

    return jsonify({'error': False, 'message': "email has been updated"}), 200

    
@auth.patch("/update_password")
@jwt_required()
def update_password():
    user_id = get_jwt_identity()
    old_password = request.get_json().get('old_password',None)
    new_password = request.get_json().get('new_password',None)

    if old_password == None:
        return jsonify({'error': True, 'message': "old_password is missing"}), 400
    if new_password == None:
        return jsonify({'error': True, 'message': "new_password is missing"}), 400  
    if len(new_password) < 5:
        return jsonify({'error': True, 'message': "new_password length must be greater than 4"}), 400

    user_attr = User.get_user_with_id(user_id)
    valid_password = check_password_hash(user_attr['password'], old_password)
    if not valid_password:
        return jsonify({'error': True, 'message': "invalid credientials"}), 400
    
    updated = User.update_password(user_id, new_password)

    return jsonify({'error': False, 'message': "password has been updated"}),200
    

@auth.patch("/update_name")
@jwt_required()
def update_name():
    user_id = get_jwt_identity()
    new_name = request.get_json().get('new_name', None)

    if new_name == None:
        return jsonify({'error': True, 'message': "new_name is missing"}), 400
    if len(new_name) < 2:
        return jsonify({'error': True, 'message': "name length should be greater than 1"}), 400

    updated = User.update_name(user_id, new_name)

    return jsonify({'error': False, 'message': "name has been updated"}),200



@auth.delete("/delete_user")
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    deleted = User.delete_user(user_id)
    if deleted:
        return jsonify({'error': False, 'message': f'user {user_id} has been deleted'}), 200
    return jsonify({'error': True, 'message': "user does not exist"}), 404
