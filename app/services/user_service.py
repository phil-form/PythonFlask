import bcrypt

from app import db
from flask import request
from app.dtos.user_dto import UserDTO
from app.forms.users.user_register_form import UserRegisterForm
from app.forms.users.user_update_form import UserUpdateForm
from app.framework.auth_service import AuthService
from app.framework.decorators.inject import inject
from app.models.role import Role
from app.services.role_service import RoleService
from app.models.user import User
from app.models.user_roles import UserRoles


class UserService:
    @inject
    def __init__(self, role_service: RoleService):
        self.role_service = role_service

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
        base_role = Role.query.filter_by(name="USER").one()
        user_role = UserRoles(user=user, role=base_role)
        user.user_roles.append(user_role)
        db.session.add(user)
        db.session.commit()
        return UserDTO(user)

    def update(self, id, form: UserUpdateForm):
        user = User.query.filter_by(userid=id).first()
        if not user:
            return None
        
        user.lastname = form.lastname.data
        user.firstname = form.firstname.data

        for roleid in form.roles.data:
            role = self.role_service.find_one_entity(int(roleid))
            # je regarde si le role existe déjà pour l'utilisateur
            if not role.name in user.roles:
                user_role = UserRoles(user=user, role=role)
                user.user_roles.append(user_role)
                db.session.add(user_role)

            # je regarde si un role doit être supprimé
            roles_to_delete = []
            for user_role in user.user_roles:
                if not str(user_role.role.id) in form.roles.data:
                    roles_to_delete.append(user_role)

            for user_role in roles_to_delete:
                user.user_roles.remove(user_role)
                db.session.delete(user_role)

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