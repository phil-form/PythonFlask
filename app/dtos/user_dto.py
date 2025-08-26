from copy import deepcopy
from app.models.user import User


class UserDTO:
    def __init__(self, user: User):
        self.username = user.username
        self.password = user.password

    def serialize(self):
        dto = deepcopy(self)
        
        return dto.__dict__
