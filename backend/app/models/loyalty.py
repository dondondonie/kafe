from app import db
from datetime import datetime

class LoyaltyPoints(db.Model):
    __tablename__ = 'loyalty_points'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False, unique=True)
    total_points = db.Column(db.Integer, default=0)
    available_points = db.Column(db.Integer, default=0)
    redeemed_points = db.Column(db.Integer, default=0)
    tier = db.Column(db.String(50), default='bronze')  # bronze, silver, gold, platinum
    points_per_dollar = db.Column(db.Float, default=1.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<LoyaltyPoints {self.customer_id}>'
