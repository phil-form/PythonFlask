from statistics import quantiles

from app import db
from app.dtos.basket_dto import BasketItemDTO
from app.forms.basket_item.basket_item_form import BasketItemForm
from app.forms.basket_item.basket_item_update import BasketItemUpdateForm
from app.framework.auth_service import AuthService
from app.framework.decorators.inject import inject
from app.models.basket_item import BasketItem
from app.models.product import Product
from app.models.user import User
from app.services.base_service import BaseService
from app.services.role_service import RoleService


class BasketItemService(BaseService):
    @inject
    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def find_all(self):
        return [BasketItemDTO(b) for b in BasketItem.query.all()]

    def find_one(self, id):
        basketItem = BasketItem.query.get(id)

        if not basketItem:
            return None

        return BasketItemDTO(basketItem)

    def find_one_by_user(self):
        user = self.auth_service.get_current_user()
        return [BasketItemDTO(b) for b in BasketItem.query.filter_by(user=user, active=True)]

    def insert(self, form: BasketItemForm):
        user = self.auth_service.get_current_user()
        if not user:
            raise TypeError

        product = Product.query.get(form.productid.data)
        if not product:
            raise TypeError

        basket_item = BasketItem(quantity=form.quantity.data, user=user, product=product)
        db.session.add(basket_item)
        db.session.commit()

        return BasketItemDTO(basket_item)


    def update(self, id, form: BasketItemUpdateForm):
        basket_item = BasketItem.query.get(id)

        if not basket_item:
            return None

        if basket_item.user.id != self.auth_service.get_current_user().id:
            return None

        basket_item.quantity = form.quantity.data

        return BasketItemDTO(basket_item)


    def delete(self, id):
        basket_item = BasketItem.query.get(id)
        if not basket_item:
            return None

        if basket_item.user.id != self.auth_service.get_current_user().id:
            return None

        basket_item.active = False
        db.session.commit()

        return BasketItemDTO(basket_item)