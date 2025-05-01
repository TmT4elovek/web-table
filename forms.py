from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, Length
import email_validator


class LoginForm(FlaskForm):
    username    = StringField('Login', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit      = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired()])
    email     = EmailField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', "The passwords you entered don't equal"), Length(8, 25)])
    password2 = PasswordField('Confirm the password', validators=[DataRequired()])
    submit    = SubmitField('Register')


class NoteForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired(), Length(1, 30)])
    tag  = RadioField('Choose tag', validators=[DataRequired()])
    submit = SubmitField('Submit')