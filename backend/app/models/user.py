from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255))
    oauth_provider = db.Column(db.String(50))  # google, github, etc
    oauth_id = db.Column(db.String(255), unique=True, index=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    avatar_url = db.Column(db.String(500))
    role = db.Column(db.String(20), default='customer')  # admin, staff, customer
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = db.relationship('Customer', backref='user', uselist=False)
    employee = db.relationship('Employee', backref='user', uselist=False)
    orders = db.relationship('Order', backref='user', lazy='dynamic')
    reservations = db.relationship('Reservation', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
