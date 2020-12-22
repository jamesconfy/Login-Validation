from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from db import *

class RegistratrionForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = StringField('Date of Birth')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    phone_no = StringField('Phone Number')
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        db = DB()
        user = db.GetByUsername(username.data)

        if user:
            raise ValidationError('This username already exists')

    def validate_email(self, email):
        db = DB()
        user = db.GetByEmail(email.data)

        if user:
            raise ValidationError('This email already exists')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = StringField('Date of Birth')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    phone_no = StringField('Phone Number')
    submit = SubmitField('Update')

    def validate_username(self, username):
        db = DB()
        if db.GetByUsername(username.data) != None:
            if username.data != db.GetByUsername(username.data)[1]:
                user = db.GetByUsername(username.data)

                if user:
                    raise ValidationError('This username already exists')

    def validate_email(self, email):
        db = DB()
        if db.GetByEmail(email.data) != None:
            if email.data != db.GetByEmail(email.data)[3]:
                user = db.GetByEmail(email.data)

                if user:
                    raise ValidationError('This email already exists')