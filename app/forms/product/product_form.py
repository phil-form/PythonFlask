from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ProductForm(FlaskForm):
    class Meta:
        csrf = False
    name = StringField('name', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])
    price = StringField('price', validators=[DataRequired()])
    quantity = StringField('quantity', validators=[DataRequired()])
