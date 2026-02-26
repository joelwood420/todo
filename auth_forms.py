from wtforms import Form, StringField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(Form):
    username = StringField('Username', [DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', [DataRequired(), Length(min=4)])

class RegisterForm(Form):
    username = StringField('Username', [DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), Length(min=4)])

class TodoForm(Form):
    title = StringField('Title', [DataRequired(), Length(max=140)])
    description = TextAreaField('Description')
    completed = BooleanField('Completed')
