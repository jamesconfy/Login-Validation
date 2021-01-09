from typing import Optional
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, ValidationError
from db import *
from datetime import date

class RegistratrionForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password Must Match')])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    dob = DateField('Date of Birth')
    address = StringField('Address')
    city = StringField('City')
    state = StringField('State')
    phone_no = StringField('Phone Number', validators=[Regexp(regex="^((\+234|0)[7-9][0-1]\d{8}$)|^()", message="Invalid Number")])
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

    
    def validate_phone_no(self, phone_no):
        numb = phone_no.data
        if len(numb) == 14:
            numb1 = numb[0:6]
            if numb1 != "+23470":
                if numb1 != "+23480":
                    if numb1 != "+23490":
                        if numb1 != "+23481":
                            raise ValidationError('Invalid Phone Number, Number should start with +23470/+23480/+23490/+23481')
            #elif numb1 == "+23491":
             #   raise ValidationError('No number starting with +23491')

        elif len(numb) == 11:
            numb1 = numb[0:3]
            if numb1 != "070":
                if numb1 != "080":
                    if numb1 != "090":
                        if numb1 != "081":
                            raise ValidationError('Invalid Phone Number, Number should start with 070/080/090/081')
            #elif numb1 == "091":
             #   raise ValidationError('No number starting with 091')
        
        elif len(numb) >= 15 or len(numb) <= 10:
            if len(numb) >= 1:
                raise ValidationError('Number Should be in format +234XXXXXXXXXX or 0XXXXXXXXXX')

    def validate_dob(self, dob):
        if dob.data >= date.today():
            raise ValidationError('Enter a date less than ' + str(date.today()))

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