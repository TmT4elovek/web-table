from flask import Flask
from flask_restful import Api

import API_Users_resources
import API_Notes_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_table_project_yml'
app.config['HOST'] = '127.0.0.1'
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300

with app.app_context():
    from routes_front import front
    from auth import auth
    from Entity import db_session
    
    db_session.global_init('database.sqlite')

    app.register_blueprint(front)
    app.register_blueprint(auth)

api = Api(app)
#users api
api.add_resource(API_Users_resources.UserResource, '/api/users/<int:user_id>+<key>')
api.add_resource(API_Users_resources.UserListResource, '/api/users/<key>')
#notes api
api.add_resource(API_Notes_resources.NoteResource, '/api/notes/<int:note_id>+<key>')
api.add_resource(API_Notes_resources.NoteListResource, '/api/notes/<key>')


if __name__ == '__main__':
    app.run(app.config['HOST'], '8080', debug=True)