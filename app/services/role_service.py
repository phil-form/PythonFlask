from app import db
from app.dtos.role_dto import RoleDTO
from app.models.role import Role
from app.services.base_service import BaseService


class RoleService(BaseService):
    def find_all(self):
        return [RoleDTO(r) for r in Role.query.all()]

    def find_one(self, id):
        return RoleDTO(Role.query.get(id))

    def find_one_entity(self, id):
        return Role.query.get(id)

    def find_all_active_entities(self):
        return Role.query.all()

    def insert(self, form):
        role = Role()
        role.name = form.name.data

        db.session.add(role)
        db.session.commit()

        return RoleDTO(role)

    def update(self, id, form):
        role = Role.query.get(id)
        role.name = form.name.data

        db.session.commit()
        return RoleDTO(role)

    def delete(self, id):
        role = Role.query.get(id)
        role.active = False

        db.session.commit()
        return RoleDTO(role)
