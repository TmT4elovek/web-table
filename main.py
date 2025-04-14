from flask import Flask, redirect, render_template
from flask_restful import Api
from flask_login import LoginManager, login_user

from Entity import db_session, __all_entities
from forms import LoginForm
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


# Login and Logout
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
async def load_user(user_id):
    session = db_session.create_session()
    return session.query(__all_entities.User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(__all_entities.User).filter(__all_entities.User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Log in', form=form, message='Неверный логин или пароль')
    return render_template('login.html', title='Log in', form=form)


if __name__ == '__main__':
    app.run('127.0.0.1', '8080', debug=True)