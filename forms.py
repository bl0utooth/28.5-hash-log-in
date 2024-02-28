from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired

class UserForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])

class TweetForm(FlaskForm):
    username = StringField('Username', validators = [InputRequired()])
    title = StringField('Title', validators = [InputRequired(), Length(max = 100)])
    text = StringField('Tweet Text', validators = [InputRequired()])

class DeleteForm(FlaskForm):
    