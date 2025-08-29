from copy import deepcopy

from app.dtos.abstract_dto import BaseDTO
from app.models.user import User


class UserDTO(BaseDTO):
    def __init__(self, user: User):
        self.id = user.userid
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.fullname = f"{user.firstname} {user.lastname}" if user.firstname and user.lastname else None
        self.roles = user.roles if user.roles else []

    def serialize(self):
        dto = deepcopy(self)
        
        return dto.__dict__
