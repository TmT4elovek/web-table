from flask import Flask
from flask_restful import Api
from flask_login import LoginManager

import requests

from Entity import db_session, __all_entities
from routes_front import front

import API_Users_resources

app = Flask(__name__)
app.config['SECRET_KEY'] = 'web_table_project_yml'
app.config['HOST'] = '127.0.0.1'
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 300
app.register_blueprint(front)

api = Api(app)
#users api
api.add_resource(API_Users_resources.UserResource, '/api/users/<int:user_id>')
api.add_resource(API_Users_resources.UserListResource, '/api/users')
#notes api
...

db_session.global_init('database.sqlite')


# Login and Logout
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(__all_entities.User).filter(__all_entities.User.id == user_id).first()



if __name__ == '__main__':
    app.run(app.config['HOST'], '8080', debug=True)