from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from app import db
from app.models import Order, OrderItem, Product, User
from app.routes import orders_bp
import uuid

@orders_bp.route('', methods=['GET'])
@jwt_required()
def get_orders():
    """Get orders"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=user_id).all()
    
    return {
        'orders': [{
            'id': o.id,
            'order_number': o.order_number,
            'status': o.status,
            'total_amount': o.total_amount,
            'final_amount': o.final_amount,
            'payment_method': o.payment_method,
            'created_at': o.created_at.isoformat()
        } for o in orders]
    }, 200

@orders_bp.route('', methods=['POST'])
@jwt_required()
def create_order():
    """Create new order"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    order = Order(
        user_id=user_id,
        order_number=f"ORD-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}",
        payment_method=data.get('payment_method'),
        notes=data.get('notes')
    )
    
    total = 0
    for item in data.get('items', []):
        product = Product.query.get(item.get('product_id'))
        if not product:
            return {'error': f"Product {item.get('product_id')} not found"}, 404
        
        quantity = item.get('quantity', 1)
        subtotal = product.price * quantity
        total += subtotal
        
        order_item = OrderItem(
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price,
            subtotal=subtotal,
            special_instructions=item.get('special_instructions')
        )
        order.items.append(order_item)
    
    order.total_amount = total
    discount = data.get('discount', 0)
    order.discount = discount
    order.final_amount = total - discount
    
    db.session.add(order)
    db.session.commit()
    
    return {
        'id': order.id,
        'order_number': order.order_number,
        'final_amount': order.final_amount,
        'message': 'Order created successfully'
    }, 201

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order details"""
    order = Order.query.get(order_id)
    
    if not order:
        return {'error': 'Order not found'}, 404
    
    return {
        'id': order.id,
        'order_number': order.order_number,
        'status': order.status,
        'total_amount': order.total_amount,
        'discount': order.discount,
        'final_amount': order.final_amount,
        'payment_method': order.payment_method,
        'items': [{
            'product_id': item.product_id,
            'product_name': item.product.name,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'subtotal': item.subtotal
        } for item in order.items],
        'created_at': order.created_at.isoformat()
    }, 200

@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get(order_id)
    
    if not order:
        return {'error': 'Order not found'}, 404
    
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'completed', 'cancelled']:
        return {'error': 'Invalid status'}, 400
    
    order.status = new_status
    if new_status == 'completed':
        order.completed_at = datetime.utcnow()
    
    db.session.commit()
    
    return {'message': 'Order status updated successfully'}, 200
