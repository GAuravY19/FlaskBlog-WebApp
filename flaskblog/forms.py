from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from flask_login import current_user
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flaskblog.models import User

class RegisterationForm(FlaskForm):
    username = StringField("Username : ", validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('EMail : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password :', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        name = User.query.filter_by(username = username.data).first()

        if name:
            raise ValidationError('Username already Exists! Please try another')


    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()

        if email:
            raise ValidationError('Email already Exists! Please try another.')



class LoginForm(FlaskForm):
    email = StringField('Email : ', validators=[DataRequired(), Email()])
    password = PasswordField('Password : ',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')



class ProfileUpdate(FlaskForm):
    username = StringField("Username : ", validators=[DataRequired(), Length(min = 2, max = 20)])
    email = StringField('EMail : ', validators=[DataRequired(), Email()])
    picture = FileField('Upload Profile picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            name = User.query.filter_by(username = username.data).first()

            if name:
                raise ValidationError('Username already Exists! Please try another')


    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email = email.data).first()

            if email:
                raise ValidationError('Email already Exists! Please try another.')



class NewPosts(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create')
