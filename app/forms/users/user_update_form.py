from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class UserUpdateForm(FlaskForm):
    class Meta:
        csrf = False
    password = StringField('password')
    lastname = StringField('lastname', validators=[DataRequired()])
    firstname = StringField('firstname', validators=[DataRequired()])