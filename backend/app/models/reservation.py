from app import db
from datetime import datetime

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reservation_number = db.Column(db.String(50), unique=True, nullable=False)
    guest_count = db.Column(db.Integer, nullable=False)
    reservation_date = db.Column(db.DateTime, nullable=False, index=True)
    reservation_time = db.Column(db.Time, nullable=False)
    duration = db.Column(db.Integer, default=60)  # in minutes
    table_number = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid
    payment_method = db.Column(db.String(50))  # cash, online
    deposit_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float)
    special_requests = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    payment = db.relationship('Payment', backref='reservation', uselist=False)
    
    def __repr__(self):
        return f'<Reservation {self.reservation_number}>'
