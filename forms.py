from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo
import email_validator


class LoginForm(FlaskForm):
    username    = StringField('Login', validators=[DataRequired()])
    password    = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit      = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username  = StringField('Username', validators=[DataRequired()])
    email     = EmailField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', "The passwords you entered don't equal")])
    password2 = PasswordField('Confirm the password', validators=[DataRequired()])
    submit    = SubmitField('Register')