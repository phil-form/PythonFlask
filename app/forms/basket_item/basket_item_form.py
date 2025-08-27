from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.validators import DataRequired


class BasketItemForm(FlaskForm):
    class Meta:
        csrf = False
    userid = IntegerField(validators=[DataRequired()])
    productid = IntegerField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])
