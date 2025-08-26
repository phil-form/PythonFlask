from flask import jsonify, request

from app.forms.users.user_register_form import UserRegisterForm
from app import app
from app.forms.users.user_update_form import UserUpdateForm
from app.services.user_service import UserService


@app.get('/users')
def get_users():
    user_service = UserService()
    return jsonify([u.serialize() for u in user_service.find_all()])

@app.get('/users/<int:userid>')
def get_user(userid: int):
    user_service = UserService()
    user = user_service.find_one(userid)
    return jsonify(user.serialize()) if user else ('', 404)

@app.post('/users')
def post_user():
    user_service = UserService()
    form = UserRegisterForm.from_json(request.json)
    
    if form.validate():
        user = user_service.insert(form)
        
        return jsonify(user.serialize())
    
    return jsonify(form.errors)

# localhost:2344/users/25
@app.put('/users/<int:userid>')
def put_user(userid: int):
    user_service = UserService()
    form = UserUpdateForm.from_json(request.json)
    
    if form.validate():
        user = user_service.update(userid, form)

        return jsonify(user.serialize())
    
    return jsonify(form.errors)

@app.delete('/users/<int:userid>')
def delete_user(userid: int):
    user_service = UserService()
    user = user_service.find_one(userid)
    if user:
        user_service.delete(user)
        return ('', 204)
    return ('', 404)
