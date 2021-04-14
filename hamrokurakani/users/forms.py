from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from hamrokurakani.models import User
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class RegistrationForm(FlaskForm):
    fullname = StringField('Name', validators=[
                           DataRequired(), Length(min=1, max=20)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_fullname(self, fullname):
        user = User.query.filter_by(fullname=fullname.data).first()
        if user:
            raise ValidationError(
                'This name is kinda taken already. Please try another.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'This username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email has already been registered. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    fullname = StringField('Name', validators=[
                           DataRequired(), Length(min=1, max=20)])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    #age = IntegerField('Age', validators=[DataRequired()])
    #gender = RadioField('Gender',choices=[('F', 'FEMALE') , ('M','MALE')], validators=[DataRequired("Please Select Your Gender!")])
    bio = StringField('Bio', validators=[
                      DataRequired(), Length(min=0, max=100)])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['png', 'jpg'])])
    submit = SubmitField('Update')

    def validate_fullname(self, fullname):
        if fullname.data != current_user.fullname:
            user = User.query.filter_by(fullname=fullname.data).first()
            if user:
                raise ValidationError(
                    'This name is kinda taken already. Please try another.')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'This username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'This email has already been registered. Please choose a different one.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError(
                'There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
