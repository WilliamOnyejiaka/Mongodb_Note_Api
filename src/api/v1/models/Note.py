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
        if query:
            return SerializeData(query, needed_attributes).serialize()
        return {}

    @staticmethod
    def get_notes(user_id, needed_attributes=['_id', 'title', 'body', 'user_id', 'created_at', 'updated_at']):
        query = list(notes.find({'user_id': user_id}).sort('_id'))

        if query:
            data = []
            for index in range(len(query)):
                note = SerializeData(
                    query[index], needed_attributes).serialize()
                data.append(note)
            return data
        return []

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
            }
        }, {'title': {
            '$regex': search_string,
            "$options": 'i'
        }}]}).sort('_id'))
        data = []

        for index in range(len(query)):
            note = SerializeData(query[index], needed_attributes).serialize()
            data.append(note)
        
        return data
