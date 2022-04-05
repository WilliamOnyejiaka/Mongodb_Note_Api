from sqlite3 import Date
from werkzeug.security import generate_password_hash
from . import db
from datetime import datetime
from src.modules.SerializeData import SerializeData
from bson.objectid import ObjectId
from .Note import Note

users = db.users


class User:

    @staticmethod
    def create_user(name, email, password):
        password = generate_password_hash(password)
        db_response = users.insert_one(
            {'name': name, 'email': email, 'password': password, 'created_at': datetime.now(), 'updated_at': None})
        return True if db_response.inserted_id else False

    @staticmethod
    def get_user(email, needed_attributes=['_id', 'name', 'email', 'password', 'created_at', 'updated_at']):
        query = users.find_one({'email': email})
        if query:
            return SerializeData(needed_attributes).serialize(query)
        return {}
    
    @staticmethod
    def get_user_with_id(id, needed_attributes=['_id', 'name', 'email', 'password', 'created_at']):
        query = users.find_one({'_id': ObjectId(id)})
        if query:
            return SerializeData(needed_attributes).serialize(query)
        return {}

    @staticmethod
    def update_email(user_id,email):
        query = users.update_one({'_id': ObjectId(user_id)}, {'$set': {'email': email,'updated_at':datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def update_password(user_id,new_password):
        new_password = generate_password_hash(new_password)
        query = users.update_one({'_id': ObjectId(user_id)}, {
                                 '$set': {'password': new_password, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def update_name(user_id,new_name):
        query = users.update_one({'_id': ObjectId(user_id)}, {
                                 '$set': {'name': new_name, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def delete_user(user_id):
        query = users.find_one_and_delete({'_id':ObjectId(user_id)})
        if query:
            user_notes = Note.get_notes(user_id)
            for index in range(len(user_notes)):
                deleted = Note.delete_note(user_notes[index]['_id'])
            return True
        return False