from datetime import datetime

import bcrypt
import jwt

from app.dtos.user_token_dto import UserTokenDTO
from app.framework.forms.user_login_form import UserLoginForm
from app.framework.auth_service import AuthService
from app.framework.models.user_base import UserBase
from app.models.user import User
from app import app


class AuthServiceImpl(AuthService):
    def __init__(self):
        super().__init__()
        self.__curent_user = None

    def login(self, user: User, form: UserLoginForm):
        # checkpw :
        # le premiere argument c'est le password non hashé passé dans le formulaire par l'utilisateur
        # le second argument c'est le password hashé se trouvant en DB
        if not bcrypt.checkpw(form.password.data.encode('utf-8'), user.password):
            raise Exception('Invalid password')

        dto = UserTokenDTO(user)
        token = jwt.encode(
            dto.serialize(),
            app.config['SECRET_KEY'],
            "HS256"
        )

        return token

    def get_current_user(self) -> User:
        print("GET CURRENT USER")
        return self.__current_user

    def set_current_user(self, tokenUser: dict) -> User:
        user = User.query.get(tokenUser['userid'])
        print("SET CURRENT USER", user)
        self.__current_user = user

        return self.__current_user

    def check_rights(self, user: UserBase, level, or_is_current_user, request_userid, **auth_kwags) -> bool:
        # appeller les check right de base du parent
        if not super().check_rights(user, level, or_is_current_user, request_userid, **auth_kwags):
            return False

        # custom rights
        return True