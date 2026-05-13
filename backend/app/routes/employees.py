from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Employee, User
from app.routes import employees_bp

def admin_required(f):
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated

@employees_bp.route('', methods=['GET'])
@admin_required
def get_employees():
    """Get all employees"""
    employees = Employee.query.filter_by(is_active=True).all()
    
    return {
        'employees': [{
            'id': e.id,
            'employee_id': e.employee_id,
            'user_id': e.user_id,
            'name': f"{e.user.first_name} {e.user.last_name}",
            'position': e.position,
            'department': e.department,
            'email': e.user.email,
            'phone': e.phone,
            'hire_date': e.hire_date.isoformat(),
            'contract_type': e.contract_type
        } for e in employees]
    }, 200

@employees_bp.route('/<int:employee_id>', methods=['GET'])
@admin_required
def get_employee(employee_id):
    """Get employee details"""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    return {
        'id': employee.id,
        'employee_id': employee.employee_id,
        'user_id': employee.user_id,
        'name': f"{employee.user.first_name} {employee.user.last_name}",
        'position': employee.position,
        'department': employee.department,
        'salary': employee.salary,
        'hourly_rate': employee.hourly_rate,
        'email': employee.user.email,
        'phone': employee.phone,
        'address': employee.address,
        'hire_date': employee.hire_date.isoformat(),
        'contract_type': employee.contract_type,
        'emergency_contact': employee.emergency_contact,
        'emergency_phone': employee.emergency_phone
    }, 200

@employees_bp.route('', methods=['POST'])
@admin_required
def create_employee():
    """Create new employee"""
    data = request.get_json()
    
    # Create user account
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        role='staff'
    )
    
    db.session.add(user)
    db.session.flush()  # Get the user ID
    
    # Create employee record
    employee = Employee(
        user_id=user.id,
        employee_id=data.get('employee_id'),
        position=data.get('position'),
        department=data.get('department'),
        salary=data.get('salary'),
        hourly_rate=data.get('hourly_rate'),
        hire_date=data.get('hire_date'),
        contract_type=data.get('contract_type'),
        phone=data.get('phone'),
        address=data.get('address'),
        emergency_contact=data.get('emergency_contact'),
        emergency_phone=data.get('emergency_phone')
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return {
        'id': employee.id,
        'employee_id': employee.employee_id,
        'message': 'Employee created successfully'
    }, 201

@employees_bp.route('/<int:employee_id>', methods=['PUT'])
@admin_required
def update_employee(employee_id):
    """Update employee"""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    data = request.get_json()
    employee.position = data.get('position', employee.position)
    employee.department = data.get('department', employee.department)
    employee.salary = data.get('salary', employee.salary)
    employee.hourly_rate = data.get('hourly_rate', employee.hourly_rate)
    employee.phone = data.get('phone', employee.phone)
    employee.address = data.get('address', employee.address)
    employee.emergency_contact = data.get('emergency_contact', employee.emergency_contact)
    employee.emergency_phone = data.get('emergency_phone', employee.emergency_phone)
    
    db.session.commit()
    
    return {'message': 'Employee updated successfully'}, 200

@employees_bp.route('/<int:employee_id>/deactivate', methods=['PUT'])
@admin_required
def deactivate_employee(employee_id):
    """Deactivate employee"""
    employee = Employee.query.get(employee_id)
    
    if not employee:
        return {'error': 'Employee not found'}, 404
    
    employee.is_active = False
    db.session.commit()
    
    return {'message': 'Employee deactivated successfully'}, 200
