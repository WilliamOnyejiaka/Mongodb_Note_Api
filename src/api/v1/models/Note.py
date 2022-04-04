from . import db
from datetime import datetime
from bson.objectid import ObjectId
from src.modules.SerializeData import SerializeData

notes = db.notes


class Note:

    @staticmethod
    def create_note(title, body, user_id):
        db_response = notes.insert_one({
            'title': title,
            'body': body,
            'user_id': user_id,
            'created_at': datetime.now(),
            'updated_at': None
        })
        return True if db_response.inserted_id else False

    @staticmethod
    def get_note(note_id, user_id, needed_attributes=['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = notes.find_one({'_id': ObjectId(note_id), 'user_id': user_id})
        return SerializeData(needed_attributes).serialize(query) if query else {} 

    @staticmethod
    def get_notes(user_id, needed_attributes=['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = list(notes.find({'user_id': user_id}).sort('_id'))
        return SerializeData(needed_attributes).dump(query) if query else []
    
    @staticmethod
    def update_title(user_id,note_id,updated_title):
        query = notes.update_one({'_id': ObjectId(note_id), 'user_id': user_id}, {'$set': {'title': updated_title, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def update_title(user_id,note_id,updated_title):
        query = notes.update_one({'_id': ObjectId(note_id), 'user_id': user_id}, {'$set': {'title': updated_title, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def update_body(user_id, note_id, updated_body):
        query = notes.update_one({'_id': ObjectId(note_id), 'user_id': user_id}, {
                                 '$set': {'body': updated_body, 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def update_note(user_id, note_id,note):
        query = notes.update_one({'_id': ObjectId(note_id), 'user_id': user_id}, {'$set': {'title': note['updated_title'], 'body': note['updated_body'], 'updated_at': datetime.now()}})
        return True if query.raw_result['nModified'] == 1 else False

    @staticmethod
    def delete_note(note_id):
        query = notes.find_one_and_delete({'_id': ObjectId(note_id)})
        return True if query else False

    @staticmethod
    def note_search(user_id, search_string, needed_attributes=['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = list(notes.find({'user_id': user_id, '$or': [{
            'body': {
                '$regex': search_string,
                "$options": 'i'
            }},
            {
            'title': {
                '$regex': search_string,
                "$options": 'i'
            }}
        ]}).sort('_id'))

        data = SerializeData(needed_attributes).dump(query)

        return data
