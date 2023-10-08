from flask_login import UserMixin
from . import db
from datetime import datetime

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email_id = db.Column(db.String(100), index=True, nullable=False)
    phone_num = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    #TODO: relationship with Event table and Booking table
    comments = db.relationship('Comment', backref='user')
    
    def __repr__(self):
        return f"Name: {self.name}"
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now().date())
    
    #TODO: add foreign key to link up with Event table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Comment: {self.text}"