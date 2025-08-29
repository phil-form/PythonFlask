import bcrypt

from app import db
from flask import request
from app.dtos.user_dto import UserDTO
from app.forms.users.user_register_form import UserRegisterForm
from app.forms.users.user_update_form import UserUpdateForm
from app.framework.auth_service import AuthService
from app.framework.decorators.inject import inject
from app.models.user import User


class UserService:
    def find_all(self):
        if len(request.args) >= 1 and request.args.get('all') == 'true':
            return [UserDTO(u) for u in User.query.all()]

        return [UserDTO(u) for u in User.query.filter_by(active=True).all()]

    def find_one(self, id):
        user = User.query.filter_by(userid=id).first()
        return UserDTO(user) if user else None

    def find_user_entity_by_username(self, username) -> User:
        user = User.query.filter_by(username=username).one()
        return user

    def insert(self, form: UserRegisterForm):
        # Un salt va être une suite de byte qui sera ajoutée au mots de passe
        # avant de le crypter
        # Donc si l'utilisateur rentre comme mots de passe Test1234=!
        # la chaine qui sera cryptée sera "Test1234=!" + SALT_RANDOM_BYTES
        salt = bcrypt.gensalt()

        user = User(
            username=form.username.data,
            password=bcrypt.hashpw(form.password.data.encode('utf8'), salt)
        )
        db.session.add(user)
        db.session.commit()
        return UserDTO(user)

    def update(self, id, form: UserUpdateForm):
        user = User.query.filter_by(userid=id).first()
        if not user:
            return None
        
        user.lastname = form.lastname.data
        user.firstname = form.firstname.data

        if form.password.data:
            # Un salt va être une suite de byte qui sera ajoutée au mots de passe
            # avant de le crypter
            # Donc si l'utilisateur rentre comme mots de passe Test1234=!
            # la chaine qui sera cryptée sera "Test1234=!" + SALT_RANDOM_BYTES
            salt = bcrypt.gensalt()
            user.password = bcrypt.hashpw(form.password.data.encode('utf8'), salt)

        db.session.commit()
        return UserDTO(user)

    def delete(self, id):
        user = User.query.filter_by(userid=id).first()
        user.active = False
        db.session.commit()
        return UserDTO(user)