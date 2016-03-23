from flask.ext.wtf import Form, RecaptchaField
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, TextAreaField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User,Activity

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64), 
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    remember_me = BooleanField('Keep me logged in', default=True)
#    recaptcha = RecaptchaField()
    submit = SubmitField('Log In')

class RegisterForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already exists')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already exists')
            
class LobbyCreateForm(Form):
    name = StringField('Lobby Name', validators=[Required(),Length(3-10)])
    description = TextAreaField('Description', validators=[Required()])
#    lobby_type = TO_BE_ADDED
    max_entries = IntegerField('Maximum Entries allowed')
    date = DateField('Date')
    submit = SubmitField('Create Lobby')
    
    def validate_name(self, field):
        if Activity.query.filter_by(name=field.data).first():
            raise ValidationError('Lobby already exists')
