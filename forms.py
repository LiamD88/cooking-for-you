from flask_wtf import FlaskForm
from wtforms import Form, StringField, validators, PasswordField, BooleanField

class RegisterForm(FlaskForm):
    name = StringField('Name', [validators.length(min=2, max=40)])
    username = StringField('Username', [validators.length(min=3, max=20)])
    email = StringField('Email', [validators.length(min=5, max =40)])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=5, max=20)])
   


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.DataRequired()])
    email = StringField('Email', [validators.DataRequired()])
    password = PasswordField('Password', [validators.DataRequired()])
    



