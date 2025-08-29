from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class RoleForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField(validators=[DataRequired()])