from copy import deepcopy

from app.dtos.abstract_dto import BaseDTO
from app.dtos.product_dto import ProductDTO
from app.models.basket_item import BasketItem


class BasketItemDTO(BaseDTO):
    def __init__(self, basket_item: BasketItem):
        self.id = basket_item.id
        self.product = ProductDTO(basket_item.product)
        self.quantity = basket_item.quantity


    def serialize(self):
        dto = deepcopy(self)
        dto.product = self.product.serialize()
        return dto.__dict__
