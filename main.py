from flask import Flask
from flask_restful import Api

from Entity import db_session
from routes_front import front
import API_Users_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_table_project_yml'
app.register_blueprint(front)

api = Api(app)
#users api
api.add_resource(API_Users_resources.UserResource, '/api/users/<int:user_id>')
api.add_resource(API_Users_resources.UserListResource, '/api/users')
#notes api
...

db_session.global_init('database.sqlite')


if __name__ == '__main__':
    app.run('127.0.0.1', '8080', debug=True)