from flask import Blueprint, request, Response, jsonify
from src.api.v1.models import db
from src.api.v1.models.User import User
import validators
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token,jwt_required,get_jwt_identity
from bson.objectid import ObjectId

auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth.post("/sign_up")
def sign_up():
    name = request.get_json().get('name', None)
    email = request.get_json().get('email', None)
    password = request.get_json().get('password', None)

    if name == None:
        return jsonify({'error': True, 'message': "name is missing"}), 400
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
        user_attr = User.get_user(email) # add created_at
        valid_password = check_password_hash(user_attr['password'], password)
        if valid_password:
            access_token = create_access_token(identity=user_attr['_id'])
            refresh_token = create_refresh_token(identity=user_attr['_id'])
            return jsonify({
                'error': False,
                'message': "logged in",
                'user_data': {
                   'id':user_attr['_id'],
                   'email':user_attr['email'],
                   'name':user_attr['name'],
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

    return jsonify({'access_token':access_token})


@auth.delete("/delete_user")
@jwt_required()
def delete_user():
    user_id = get_jwt_identity()
    deleted = User.delete_user(user_id)
    if deleted:
        return jsonify({'error': False, 'message': f'user {user_id} has been deleted'}), 200
    return jsonify({'error': True, 'message': "user does not exist"}), 404
