from flask import jsonify, request
from app import app
from app.forms.product.product_form import ProductForm
from app.framework.decorators.auth_required import auth_required
from app.framework.decorators.inject import inject
from app.services.product_service import ProductService


@app.get('/products')
@inject
def get_all_products(product_service: ProductService):
    return jsonify([dto.serialize() for dto in product_service.find_all()])

@app.get('/products/<int:id>')
@inject
def get_product_by_id(id, product_service: ProductService):

    dto = product_service.find_one(id)
    return jsonify(dto.serialize())

@app.post('/products')
@auth_required(level="ADMIN")
@inject
def post_product(product_service: ProductService):
    form = ProductForm.from_json(request.json)
    if form.validate():
        dto = product_service.insert(form)

        return jsonify(dto.serialize())

    return jsonify(form.errors)

@app.put('/products/<int:id>')
@auth_required(level="ADMIN")
@inject
def put_product(id, product_service: ProductService):
    form = ProductForm.from_json(request.json)
    if form.validate():
        dto = product_service.update(id, form)

        return jsonify(dto.serialize()) if dto else None

    return jsonify(form.errors)

@app.delete('/products/<int:id>')
@auth_required(level="ADMIN")
@inject
def delete_product(id, product_service: ProductService):
    dto = product_service.delete(id)
    return jsonify(dto.serialize()) if dto else None