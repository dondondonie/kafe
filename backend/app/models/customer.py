from app import db
from datetime import datetime

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    city = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))
    birthday = db.Column(db.Date)
    total_spent = db.Column(db.Float, default=0)
    total_orders = db.Column(db.Integer, default=0)
    last_order_date = db.Column(db.DateTime)
    loyalty_member = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    photos = db.relationship('CustomerPhoto', backref='customer', lazy='dynamic')
    loyalty_points = db.relationship('LoyaltyPoints', backref='customer', uselist=False)
    
    def __repr__(self):
        return f'<Customer {self.user_id}>'

class CustomerPhoto(db.Model):
    __tablename__ = 'customer_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    photo_url = db.Column(db.String(500), nullable=False)
    caption = db.Column(db.Text)
    product_purchased = db.Column(db.String(255))  # The coffee/product they bought
    is_featured = db.Column(db.Boolean, default=False)
    likes = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<CustomerPhoto {self.id}>'
