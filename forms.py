from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class UserForm(FlaskForm):
    """username and password fields."""
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    first_name = StringField('First_name', validators=[InputRequired()])
    last_name = StringField('Last_name', validators=[InputRequired()])

#secret text form
class SecretForm(FlaskForm):
    """Just a simple text saying you made it."""
    text = StringField('Text', validators=[InputRequired()])
    