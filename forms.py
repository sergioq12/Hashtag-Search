from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # input fields
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")

class RegisterForm(FlaskForm):
    # input fields
    username = StringField("Username",validators=[DataRequired()])
    password = PasswordField("Password",validators=[DataRequired()])
    re_password = PasswordField("Repeat Password",validators=[DataRequired()])
    email = StringField("Email",validators=[DataRequired()])
    submit = SubmitField("Register")

class SearchForm(FlaskForm):
    # input field
    search = StringField("Search Hashtag",validators=[DataRequired()])
    submit = SubmitField("Search")