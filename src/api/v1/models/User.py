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
    def get_user(email, needed_attributes=['_id', 'name', 'email', 'password', 'created_at']):
        query = users.find_one({'email': email})
        if query:
            return SerializeData(needed_attributes).serialize(query)
        return {}

    @staticmethod
    def delete_user(user_id):
        query = users.find_one_and_delete({'_id':ObjectId(user_id)})
        if query:
            user_notes = Note.get_notes(user_id)
            for index in range(len(user_notes)):
                deleted = Note.delete_note(user_notes[index]['_id'])
            return True
        return False