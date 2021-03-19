from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User

class Form(FlaskForm):
    query = StringField('Search YouTube', validators=[DataRequired()])
    #submit = SubmitField('Go!')
    
class RequestForm(FlaskForm):
    artist = StringField('Artist', validators=[DataRequired(message="아티스트 정보를 입력해주세요")])
    title = StringField('Title', validators=[DataRequired(message="제목을 입력해주세요")])
    requester = StringField('Requester', validators=[DataRequired(message="신청자 정보를 남겨주세요")])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')