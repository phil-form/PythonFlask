from app import db
from app.framework.models.role_base import RoleBase
from app.models.base_entity import BaseEntity


class Role(db.Model, RoleBase, BaseEntity):
    __tablename__ = 'roles'

    user_roles = db.relationship('UserRoles', back_populates='role')