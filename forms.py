from flask_wtf import FlaskForm
from wtforms import Form, Stringfield, validators, PasswordField, BooleanField

class RegisterForm(Form):
    name = Stringfield('Name', [validators.length(min=2, max= 40)])
    username = Stringfield('Username', [validators.length(min=3, max =20)])
    email = Stringfield('Email', [validators.length(min=5, max =40)])
    password = PasswordField('Password', [validators.DataRequired(), validators.length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired(), validators.length(min=5, max=20)], validators.Equalto('password', message = "Passwords must match."))





