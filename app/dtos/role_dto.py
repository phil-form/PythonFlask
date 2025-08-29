from app.dtos.abstract_dto import BaseDTO


class RoleDTO(BaseDTO):
    def __init__(self, role):
        self.id = role.id
        self.name = role.name

    def serialize(self):
        return self.__dict__

