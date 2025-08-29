from app.dtos.abstract_dto import BaseDTO
from app.models.product import Product


class ProductDTO(BaseDTO):
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.description = product.description
        self.price = product.price
        self.quantity = product.quantity

    def serialize(self):
        return self.__dict__
