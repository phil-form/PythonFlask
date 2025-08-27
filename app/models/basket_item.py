from app import db
from app.models.base_entity import BaseEntity


class BasketItem(db.Model, BaseEntity):
    __tablename__ = 'baskets'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.userid'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    user = db.relationship('User', back_populates='basket_items')
    product = db.relationship('Product')