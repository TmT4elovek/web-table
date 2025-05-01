from flask import jsonify, current_app

from flask_restful import abort, reqparse, Resource
from flask_bcrypt import generate_password_hash

from Entity import db_session
from Entity.__all_entities import Note


def abort_if_note_is_not_found(note_id):
    session = db_session.create_session()
    note = session.query(Note).filter(Note.id == note_id).first()
    if not note:
        abort(404, message=f'Note with id {note_id} not found.')
    return note


class NoteResource(Resource):
    def get(self, note_id, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        note = abort_if_note_is_not_found(note_id)
        return jsonify({'note': note.to_dict(only=('id', 'user_id', 'tag_id', 'text'))})
    
    def delete(self, note_id, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        note = abort_if_note_is_not_found(note_id)

        session = db_session.create_session()
        session.delete(note)

        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('text', required=True)
parser.add_argument('user_id', required=True)
parser.add_argument('tag_id', required=True)


class NoteListResource(Resource):
    def get(self, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        
        session = db_session.create_session()
        
        notes = session.query(Note).all()

        return jsonify({'notes': [note.to_dict(only=('id', 'user_id', 'tag_id', 'text')) for note in notes]})
    
    def post(self, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        session = db_session.create_session()
        args = parser.parse_args()
        note = Note(
            user_id=args['user_id'],
            text=args['text'],
            tag_id=args['tag_id']
        )
        session.add(note)
        session.commit()
        return jsonify({'id': note.id})