from app import db
from app.dtos.product_dto import ProductDTO
from app.forms.product.product_form import ProductForm
from app.models.product import Product
from app.services.base_service import BaseService


class ProductService(BaseService):
    def find_all(self):
        return [ProductDTO(p) for p in Product.query.all()]

    def find_one(self, id):
        return ProductDTO(Product.query.filter_by(id=id))

    def insert(self, form: ProductForm):
        product = Product(
            name=form.name.data,
            price=form.price.data,
            description=form.description.data,
            quantity=form.quantity.data,
        )
        db.session.add(product)
        db.session.commit()

        return ProductDTO(product)

    def update(self, id, form: ProductForm):
        product = Product.query.filter_by(id=id).first()

        if not product:
            return None

        product.name = form.name.data
        product.price = form.price.data
        product.description = form.description.data
        product.quantity = form.quantity.data

        db.session.commit()
        return ProductDTO(product)

    def delete(self, id):
        product = Product.query.filter_by(id=id).one()
        if not product:
            return None

        db.session.delete(product)
        db.session.commit()
        return ProductDTO(product)
