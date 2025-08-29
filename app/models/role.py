from app import db
from app.framework.models.role_base import RoleBase


class Role(db.Model, RoleBase):
    __tablename__ = 'roles'

    user_roles = db.relationship('UserRoles', back_populates='role')