from app import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
    quantity = db.Column(db.Integer, default=0)
    unit = db.Column(db.String(50), default='units')  # kg, liters, units, etc
    min_stock = db.Column(db.Integer, default=10)
    max_stock = db.Column(db.Integer, default=100)
    reorder_level = db.Column(db.Integer, default=20)
    last_restock = db.Column(db.DateTime)
    last_restock_quantity = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_low_stock(self):
        return self.quantity <= self.reorder_level
    
    def __repr__(self):
        return f'<Inventory {self.product_id}>'
