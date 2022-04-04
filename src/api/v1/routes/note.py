from turtle import update
from flask import Blueprint, request, jsonify
from src.api.v1.models.Note import Note, notes
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.modules.Pagination import Pagination

note = Blueprint("note", __name__, url_prefix="/api/v1/note")


@note.post("/create_note")
@jwt_required()
def create_note():
    title = request.get_json().get('title', None)
    body = request.get_json().get('body', "")
    user_id = get_jwt_identity()

    if not title:
        return jsonify({'error': True, 'message': "title missing"}), 400

    note = Note.create_note(title, body, user_id)
    if note:
        return jsonify({'error': False, 'message': "note has been successfully created"}), 200

    return jsonify({'error': True, 'message': "something went wrong"}), 500


@note.get("/get_note/<id>")
@jwt_required()
def get_note(id):
    user_id = get_jwt_identity()
    note = Note.get_note(id, user_id)

    if not note:
        return jsonify({'error': True, 'message': "note not found"}), 404
    return jsonify({'error': False, 'data': note}), 200


@note.get("/get_notes")
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    notes = Note.get_notes(user_id)

    return jsonify({'error': False, 'data': notes}), 200


@note.get("/pagination/note_pagination")
@jwt_required()
def note_pagination():
    user_id = get_jwt_identity()
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit must be an integer"}), 400

    paginate = Pagination(Note.get_notes(user_id), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200


@note.patch("/update_title/<id>")
@jwt_required()
def update_title(id):
    user_id = get_jwt_identity()
    title = request.get_json().get('title','')
    updated = Note.update_title(user_id,id,title)
    return jsonify({'error': False, 'message': "note title has been updated"}), 200

@note.patch("/update_body/<id>")
@jwt_required()
def update_body(id):
    user_id = get_jwt_identity()
    body = request.get_json().get('body', '')
    updated = Note.update_body(user_id, id, body)
    return jsonify({'error': False, 'message': "note body has been updated"}), 200


@note.put("/update_note/<id>")
@jwt_required()
def update_note(id):
    user_id = get_jwt_identity()
    title = request.get_json().get('title', '')
    body = request.get_json().get('body', '')
    updated = Note.update_note(
        user_id, id, {'updated_title': title, 'updated_body': body})
    return jsonify({'error': False, 'message': "note has been updated"}), 200

@note.delete("/delete_note/<id>")
@jwt_required()
def delete_note(id):
    deleted = Note.delete_note(id)
    if deleted:
        return jsonify({'error': False, 'message': "note has been deleted"}), 200
    return jsonify({'error': True, 'message': "something went wrong"}), 500


@note.get("/search")
@jwt_required()
def note_search():
    user_id = get_jwt_identity()
    search_string = request.args.get('search_string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search_string needed"}), 400

    data = Note.note_search(user_id, search_string)
    return jsonify({'error': False, 'data': data}), 200


@note.get("/pagination/note_search")
@jwt_required()
def note_search_pagination():
    user_id = get_jwt_identity()
    search_string = request.args.get('search_string', None)

    if not search_string:
        return jsonify({'error': True, 'message': "search_string needed"}), 400

    page = request.args.get('page', 1)
    limit = request.args.get('limit', 10)
    try:
        page = int(request.args.get('page', 1))
        limit = int(request.args.get('limit', 10))
    except Exception:
        return jsonify({'error': True, 'message': "page and limit must be an integer"}), 400
    
    paginate = Pagination(Note.note_search(user_id,search_string), page, limit).meta_data()

    return jsonify({'error': False, 'data': paginate}), 200
