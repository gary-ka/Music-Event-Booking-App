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
    
    comments = db.relationship('Comment', backref='user')
    events = db.relationship('Event', backref='user')
    bookings = db.relationship('Booking', backref='user')
    
    def __repr__(self):
        return f"Name: {self.name}"
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000))
    created_at = db.Column(db.DateTime, default=datetime.now().date())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Comment: {self.text}"
    
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    intro = db.Column(db.String(500), nullable=False)
    musician = db.Column(db.String(500), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(400))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='event')
    bookings = db.relationship('Booking', backref='event')
    
    def __repr__(self):
        return f"Event Name: {self.name}"

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    num_tickets = db.Column(db.Integer, nullable=False)
    card_name = db.Column(db.String(100), nullable=False)
    card_num = db.Column(db.Integer, nullable=False)
    cvv = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String(9), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    def __repr__(self):
        return f"Order Number: {self.id}"

