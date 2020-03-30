from app import db
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField
from flask_wtf import FlaskForm
from wtforms.fields.html5 import DateTimeLocalField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ChangelogForm(FlaskForm):
    # timestamp = DateTimeLocalField('TimeStamp', format='%Y-%m-%d %H:%M:%S')
    version = StringField('Version', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=1, max=140)])
    summary = TextAreaField('Summary', validators=[DataRequired(), Length(min=1, max=750)])
    change_type = SelectField('Type', choices=[('Added', 'Added'),('Changed', 'Changed'), ('Deprecated', 'Deprecated'), ('Removed', 'Removed'), ('Fixed', 'Fixed'), ('Security', 'Security')], validators=[DataRequired()])
    submit = SubmitField('Save')