from app import db
from app.framework.models.user_base import UserBase
from app.models.base_entity import BaseEntity


class User(db.Model, UserBase, BaseEntity):
    __tablename__ = 'users'

    lastname = db.Column(db.String(255), nullable=True)
    firstname = db.Column(db.String(255), nullable=True)

    basket_items = db.relationship('BasketItem', back_populates='user')
    user_roles = db.relationship('UserRoles', back_populates='user', cascade="all, delete-orphan")

    @property
    def roles(self):
        return [r.role.name for r in self.user_roles]