from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from app import db
from app.models import Order, User, Customer, Inventory, Reservation
from app.routes import analytics_bp
from sqlalchemy import func

def admin_required(f):
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated

@analytics_bp.route('/sales', methods=['GET'])
@admin_required
def get_sales_analytics():
    """Get sales analytics"""
    days = request.args.get('days', 30, type=int)
    start_date = datetime.utcnow() - timedelta(days=days)
    
    orders = Order.query.filter(
        Order.created_at >= start_date,
        Order.status == 'completed'
    ).all()
    
    total_sales = sum(o.final_amount for o in orders)
    total_orders = len(orders)
    avg_order_value = total_sales / total_orders if total_orders > 0 else 0
    
    # Daily sales
    daily_sales = {}
    for order in orders:
        date_key = order.created_at.date().isoformat()
        if date_key not in daily_sales:
            daily_sales[date_key] = 0
        daily_sales[date_key] += order.final_amount
    
    return {
        'period_days': days,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'avg_order_value': avg_order_value,
        'daily_sales': daily_sales
    }, 200

@analytics_bp.route('/inventory', methods=['GET'])
@admin_required
def get_inventory_analytics():
    """Get inventory analytics"""
    inventory_items = Inventory.query.all()
    
    low_stock_items = [inv for inv in inventory_items if inv.is_low_stock()]
    
    return {
        'total_items': len(inventory_items),
        'low_stock_count': len(low_stock_items),
        'low_stock_items': [{
            'product_id': inv.product_id,
            'product_name': inv.product.name,
            'quantity': inv.quantity,
            'reorder_level': inv.reorder_level
        } for inv in low_stock_items]
    }, 200

@analytics_bp.route('/customers', methods=['GET'])
@admin_required
def get_customer_analytics():
    """Get customer analytics"""
    total_customers = Customer.query.count()
    loyalty_members = Customer.query.filter_by(loyalty_member=True).count()
    
    # Top spending customers
    top_customers = db.session.query(
        Customer.id,
        Customer.total_spent
    ).order_by(Customer.total_spent.desc()).limit(10).all()
    
    return {
        'total_customers': total_customers,
        'loyalty_members': loyalty_members,
        'top_customers': [{
            'customer_id': c[0],
            'total_spent': c[1]
        } for c in top_customers]
    }, 200

@analytics_bp.route('/reservations', methods=['GET'])
@admin_required
def get_reservation_analytics():
    """Get reservation analytics"""
    pending = Reservation.query.filter_by(status='pending').count()
    confirmed = Reservation.query.filter_by(status='confirmed').count()
    completed = Reservation.query.filter_by(status='completed').count()
    cancelled = Reservation.query.filter_by(status='cancelled').count()
    
    return {
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'cancelled': cancelled
    }, 200
