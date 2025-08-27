from app import db
from app.dtos.user_dto import UserDTO
from app.forms.users.user_register_form import UserRegisterForm
from app.forms.users.user_update_form import UserUpdateForm
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

    def update(self, id, form: UserUpdateForm):
        user = User.query.filter_by(userid=id).first()
        if not user:
            return None
        
        user.lastname = form.lastname.data
        user.firstname = form.firstname.data

        if form.password.data:
            user.password = form.password.data

        db.session.commit()
        return UserDTO(user)

    def delete(self, user: User):
        db.session.delete(user)
        db.session.commit()
        return UserDTO(user)