from app import db
from datetime import datetime

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)  # barista, manager, cashier, etc
    department = db.Column(db.String(100))
    salary = db.Column(db.Float)
    hourly_rate = db.Column(db.Float)
    hire_date = db.Column(db.Date, nullable=False)
    contract_type = db.Column(db.String(50))  # full-time, part-time, contract
    phone = db.Column(db.String(20))
    address = db.Column(db.String(255))
    emergency_contact = db.Column(db.String(120))
    emergency_phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Employee {self.employee_id}>'
