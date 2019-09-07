import forms
from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import TextAreaField

from flask_wtf import FlaskForm
from wtforms import StringField
from rake_nltk import Rake
from wtforms.validators import DataRequired
from models import User

class SearchSub(Form):
    text = StringField('subreddit', validators=[DataRequired()])


class PostForm(FlaskForm):
	kw = StringField('Keyword: ', validators=[DataRequired()])
	sub = StringField('Subreddit: ', validators=[DataRequired()])

	submit = SubmitField('Post')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Reddit Username', validators=[DataRequired()])
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

class RegistrationAppForm(FlaskForm):
	app_name=StringField('App name', validators=[DataRequired()])
	client_id=StringField('Client ID', validators=[DataRequired()])
	secret=StringField('Secret', validators=[DataRequired()])
	password = PasswordField('Reddit Password', validators=[DataRequired()])
	password2 = PasswordField('Repeat Reddit Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Save App')

	def validate_username(self, username):
	    user = User.query.filter_by(username=username.data).first()
	    if user is not None:
	        raise ValidationError('Please use a different username.')

	def validate_email(self, email):
	    user = User.query.filter_by(email=email.data).first()
	    if user is not None:
	        raise ValidationError('Please use a different email address.')

class Titles(FlaskForm):
    title=StringField('title:', validators=[DataRequired()])
    author=StringField('author:', validators=[DataRequired()])
    description=TextAreaField('description:')
    submit=SubmitField('Submit')
class Chapters(Form):
    title=StringField('title:', validators=[DataRequired()])
    text=StringField('text', validators=[DataRequired()])
