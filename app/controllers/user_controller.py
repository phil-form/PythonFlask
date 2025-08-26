from flask import jsonify, request

from app.forms.users.user_register_form import UserRegisterForm
from app import app
from app.services.user_service import UserService


@app.get('/users')
def get_users():
    user_service = UserService()
    return [jsonify(u) for u in user_service.find_all()]

@app.post('/users')
def post_user():
    user_service = UserService()
    form = UserRegisterForm.from_json(request.json)
    
    if form.validate():
        user = user_service.insert(form)
        
        return jsonify(user)
    
    return jsonify(form.errors)