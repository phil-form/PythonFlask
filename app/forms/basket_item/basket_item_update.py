from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class BasketItemUpdateForm(FlaskForm):
    class Meta:
        csrf = False
    quantity = IntegerField(validators=[DataRequired()])
