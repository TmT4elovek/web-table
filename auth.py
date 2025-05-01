from flask import current_app, redirect, render_template, Blueprint

from flask_login import LoginManager, login_user, logout_user, login_required

from flask_bcrypt import generate_password_hash

from Entity import db_session
from Entity.__all_entities import User
from forms import LoginForm, RegisterForm

auth = Blueprint('Auth', __name__, static_folder='/static/')

login_manager = LoginManager()
login_manager.init_app(current_app)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).filter(User.id == user_id).first()

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Log in', form=form, message='Неверный логин или пароль', user='not_home')
    return render_template('login.html', title='Log in', form=form, user='not_home')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form, message='An account with that email already exists.', user='not_home')
        elif session.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Register', form=form, message='An account with that name already exists.', user='not_home')
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password1.data, 13).decode()
        )
        session.add(user)
        session.commit()

        login_user(user)
        return redirect('/')            
    return render_template('register.html', title='Register', form=form, user='not_home')

@current_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')