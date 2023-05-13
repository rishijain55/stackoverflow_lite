from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, ValidationError

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password')
    accid = IntegerField('Account ID')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):
    displayname = StringField('DisplayName', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    aboutme = StringField('AboutMe')
    location = StringField('Location')
    websiteurl = StringField('WebsiteURL')  
    submit = SubmitField('Sign Up')

class PostQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Post Question')

class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired()])
    newpassword = PasswordField('New Password', validators=[DataRequired()])
    confirmnewpassword = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('newpassword', message='Passwords must match')])
    submit = SubmitField('Change Password')

        
class SearchForm(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')

class EditProfileForm(FlaskForm):
    displayname = StringField('DisplayName')
    aboutme = StringField('AboutMe')
    location = StringField('Location')
    websiteurl = StringField('WebsiteURL')  
    submit = SubmitField('Edit Profile')

class EditQuestionForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    tags = StringField('Tags', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Edit Question')

class EditAnswerForm(FlaskForm):
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Edit Answer')

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')