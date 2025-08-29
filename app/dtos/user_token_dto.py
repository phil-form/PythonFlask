from datetime import datetime, timedelta

from app.dtos.abstract_dto import BaseDTO
from app.models.user import User


class UserTokenDTO(BaseDTO):
    def __init__(self, user: User):
        self.userid = user.userid
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.roles = user.roles if user.roles else []

    def serialize(self):
        self.exp = (datetime.now() + timedelta(hours=1)).timestamp()
        self.iat = datetime.now().timestamp()

        return self.__dict__

