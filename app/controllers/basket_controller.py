from flask import jsonify, request

from app import app
from app.forms.basket_item.basket_item_form import BasketItemForm
from app.forms.basket_item.basket_item_update import BasketItemUpdateForm
from app.framework.decorators.auth_required import auth_required
from app.framework.decorators.inject import inject
from app.services.basket_item_service import BasketItemService


@app.get('/baskets')
@auth_required(level="USER")
@inject
def get_baskets(basket_service: BasketItemService):
    return jsonify([bi.serialize() for bi in basket_service.find_all()])

@app.get('/baskets/<int:basket_id>')
@auth_required(level="ADMIN")
@inject
def get_one_basket(basket_id, basket_service: BasketItemService):
    basket = basket_service.find_one(basket_id)
    return jsonify(basket.serialize()) if basket else None

@app.get('/baskets/user')
@auth_required(level="USER")
@inject
def get_one_user_basket(basket_id, basket_service: BasketItemService):
    basket = basket_service.find_one_by_user()
    return jsonify(basket.serialize()) if basket else None

@app.post('/baskets')
@auth_required(level="USER")
@inject
def post_basket(basket_service: BasketItemService):
    form = BasketItemForm.from_json(request.json)

    if form.validate():
        basket = basket_service.insert(form)

        return jsonify(basket.serialize()) if basket else None

        return jsonify(form.serialize())

    return jsonify(form.errors)

@app.put('/baskets/<int:basket_id>')
@auth_required(level="USER")
@inject
def put_one_basket(basket_id, basket_service: BasketItemService):
    form = BasketItemUpdateForm.from_json(request.json)

    if form.validate():
        basket = basket_service.update(form)

        return jsonify(basket.serialize()) if basket else None

    return jsonify(form.errors)

@app.delete('/baskets/<int:basket_id>')
@auth_required(level="USER")
@inject
def delete_one_basket(basket_id, basket_service: BasketItemService):
    basket = basket_service.delete(basket_id)
    return jsonify(basket.serialize()) if basket else None