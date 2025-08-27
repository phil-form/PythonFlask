from copy import deepcopy

from app.dtos.abstract_dto import AbstractDTO
from app.models.user import User


class UserDTO(AbstractDTO):
    def __init__(self, user: User):
        self.id = user.userid
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.fullname = f"{user.firstname} {user.lastname}" if user.firstname and user.lastname else None

    def serialize(self):
        dto = deepcopy(self)
        
        return dto.__dict__
