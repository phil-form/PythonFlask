from flask import jsonify, request

from app.forms.users.user_register_form import UserRegisterForm
from app import app
from app.forms.users.user_update_form import UserUpdateForm
from app.framework.auth_service import AuthService
from app.framework.decorators.auth_required import auth_required
from app.framework.decorators.inject import inject
from app.services.user_service import UserService

@app.get('/users')
@auth_required(level="USER")
@inject
def get_users(user_service: UserService):
    return jsonify([u.serialize() for u in user_service.find_all()])

@app.get('/users/<int:userid>')
@inject
def get_user(userid: int, user_service: UserService):
    user = user_service.find_one(userid)
    return jsonify(user.serialize()) if user else ('', 404)

@app.post('/users')
@inject
def post_user(user_service: UserService):
    form = UserRegisterForm.from_json(request.json)
    
    if form.validate():
        user = user_service.insert(form)
        
        return jsonify(user.serialize())
    
    return jsonify(form.errors)

# localhost:2344/users/25
@app.put('/users/<int:userid>')
@inject
def put_user(userid: int, user_service: UserService):
    form = UserUpdateForm.from_json(request.json)
    
    if form.validate():
        dto = user_service.update(userid, form)

        return jsonify(dto.serialize()) if dto else None
    
    return jsonify(form.errors)

@app.delete('/users/<int:userid>')
@inject
def delete_user(userid: int, user_service: UserService):
    dto = user_service.delete(userid)
    return jsonify(dto.serialize()) if dto else None
