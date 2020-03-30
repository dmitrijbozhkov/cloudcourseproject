""" Form validators for authorization """
import re
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError, Email, EqualTo
from cloudcourseproject.src.model import User

def password_validator(password):
    """ Validate password should contain capital and small latin letters and numbers """
    if re.search("[0-9]", password) is None:
        raise ValidationError("Password should have numbers")
    if re.search("[A-Z]", password) is None:
        raise ValidationError("Password should contain capital latin letters")
    if re.search("[a-z]", password) is None:
        raise ValidationError("Password should contain lower latin letters")

class LoginForm(FlaskForm):
    """ Validate login request """
    email = StringField("email", validators=[
        DataRequired("Email is required"),
        Email(message="Email field should be a valid email address")
    ])
    password = PasswordField("password", validators=[
        DataRequired("Password is required"),
        Length(message="Password should be between 6 and 20 characters!", min=6, max=20)
    ])
    submit = SubmitField("Login")

    def validate_password(self, field):
        """ Perform password validation """
        password_validator(field.data)

class CreateAccountForm(FlaskForm):
    """ Validate creation of user account """
    username = StringField("username", validators=[
        DataRequired("Username is required"),
        Length(message="Password should be between 6 and 20 characters!", min=4, max=20)
    ])
    email = StringField("email", validators=[
        DataRequired("Email is required"),
        Email(message="Email field should be a valid email address")
    ])
    password = PasswordField("password", validators=[
        DataRequired("Password is required"),
        Length(message="Password should be between 6 and 20 characters!", min=6, max=20)
    ])
    confirm_password = PasswordField("confirm_password", validators=[
        DataRequired("Password confirmation is required"),
        EqualTo("password", message="Passwords aren't equal")
    ])
    submit = SubmitField("Register")

    def validate_password(self, field):
        """ Perform password validation """
        password_validator(field.data)

    def validate_username(self, field):
        """ Check if username already taken """
        result = User.query.filter_by(username=field.data).first()
        if result:
            raise ValidationError(f"Username {field.data} already taken!")

    def validate_email(self, field):
        """ Check if username already taken """
        result = User.query.filter_by(email=field.data).first()
        if result:
            raise ValidationError(f"User by email {field.data} already exists, maybe you have forgot your password?")
