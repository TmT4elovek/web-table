from flask import Blueprint, render_template, redirect, Response

from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import generate_password_hash

from Entity.__all_entities import Note, Tag, User
from Entity import db_session

from forms import LoginForm, RegisterForm

front = Blueprint('Front', __name__, static_folder='/static/')

@front.route('/', methods=['GET'])
def main():
    session = db_session.create_session()

    tags = session.query(Tag).all()
    notes=[
    ]
    return render_template('main.html', title='Home', tags=tags, notes=notes, user=current_user if isinstance(current_user, User) else None)

@front.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', title='Log in', form=form, message='Неверный логин или пароль', user='auth')
    return render_template('login.html', title='Log in', form=form, user='auth')


@front.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Register', form=form, message='An account with that email already exists.', user='auth')
        elif session.query(User).filter(User.username == form.username.data).first():
            return render_template('register.html', title='Register', form=form, message='An account with that name already exists.', user='auth')
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password1.data, 13).decode()
        )
        session.add(user)
        session.commit()

        login_user(user)
        return redirect('/')            
    return render_template('register.html', title='Register', form=form, user='auth')

@front.route('/logout')
@login_required
def logout():
    logout_user()
    redirect('/')
    return main()