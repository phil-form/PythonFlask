from app import db

class User(db.Model):
    __tablename__ = 'users'
    
    userid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=True)
    firstname = db.Column(db.String(255), nullable=True)