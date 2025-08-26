from app import db
from app.dtos.user_dto import UserDTO
from app.forms.users.user_register_form import UserRegisterForm
from app.models.user import User


class UserService:
    def find_all(self):
        return [UserDTO(u) for u in User.query.all()]

    def find_one(self, id):
        user = User.query.filter_by(userid=id).first()
        return UserDTO(user) if user else None

    def insert(self, form: UserRegisterForm):
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return UserDTO(user)

    def update(self, user: User):
        db.session.commit()
        return UserDTO(user)

    def delete(self, user: User):
        db.session.delete(user)
        db.session.commit()
        return UserDTO(user)