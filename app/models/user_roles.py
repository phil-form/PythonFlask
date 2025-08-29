from app import db

class UserRoles(db.Model):
    __tablename__ = 'user_roles'

    roleid = db.Column(db.ForeignKey('roles.id'), primary_key=True)
    userid = db.Column(db.ForeignKey('users.userid'), primary_key=True)

    user = db.relationship('User', back_populates='user_roles')
    role = db.relationship('Role', back_populates='user_roles')