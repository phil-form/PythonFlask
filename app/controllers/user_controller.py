from flask import jsonify

from app import app
from app.services.user_service import UserService


@app.get('/users')
def get_users():
    user_service = UserService()
    return [jsonify(u) for u in user_service.find_all()]