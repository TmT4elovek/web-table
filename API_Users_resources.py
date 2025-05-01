from flask import jsonify, current_app

from flask_restful import abort, reqparse, Resource
from flask_bcrypt import generate_password_hash

from Entity import db_session
from Entity.__all_entities import User



def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    user: User | None = session.query(User).filter(User.id == user_id).first()
    if not user:
            abort(404, message=f'User with id {user_id} not found.')
    return user


class UserResource(Resource):
    def get(self, user_id, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        user = abort_if_user_not_found(user_id)
        return jsonify({'user': user.to_dict(only=('id', 'username', 'email'))})
    
    def delete(self, user_id, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        user = abort_if_user_not_found(user_id)

        session = db_session.create_session()
        session.delete(user)

        session.commit()
        return jsonify({'success': 'OK'})
    

parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)
parser.add_argument('email', required=True)


class UserListResource(Resource):
    def get(self, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [
            user.to_dict(only=('id', 'username', 'email')) for user in users
        ]})
    
    def post(self, key):
        if key != current_app.config['SECRET_KEY']:
            abort(403, message='Access denied')
        session = db_session.create_session()
        args = parser.parse_args()
        user = User(
            username=args['username'],
            password=generate_password_hash(args['password']),
            email=args['email']
        )
        session.add(user)
        session.commit()
        return jsonify({'id': user.id})