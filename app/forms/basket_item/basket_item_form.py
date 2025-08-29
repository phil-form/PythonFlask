from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired

from app.framework.decorators.inject import inject
from app.services.product_service import ProductService


class BasketItemForm(FlaskForm):
    class Meta:
        csrf = False

    productid = SelectField(validators=[DataRequired()])
    quantity = IntegerField(validators=[DataRequired()])

    @inject
    def __init__(self, product_service: ProductService, *args, **kwargs):
        super(BasketItemForm, self).__init__(*args, **kwargs)
        self.product_service = product_service
        self.productid.choices = [str(product.id) for product in self.product_service.find_all_active_entities()]
