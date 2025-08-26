from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class UserRegisterForm(FlaskForm):
    class Meta:
        csrf = False
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
