from app.dtos.abstract_dto import AbstractDTO
from app.models.product import Product


class ProductDTO(AbstractDTO):
    def __init__(self, product: Product):
        self.id = product.id
        self.name = product.name
        self.description = product.description
        self.price = product.price
        self.quantity = product.quantity

    def serialize(self):
        return self.__dict__
