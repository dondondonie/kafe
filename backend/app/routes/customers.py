from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Customer, CustomerPhoto, User
from app.routes import customers_bp

@customers_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_customer_profile():
    """Get current customer profile"""
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(user_id=user_id).first()
    
    if not customer:
        return {'error': 'Customer profile not found'}, 404
    
    return {
        'id': customer.id,
        'user_id': customer.user_id,
        'phone': customer.phone,
        'address': customer.address,
        'city': customer.city,
        'postal_code': customer.postal_code,
        'country': customer.country,
        'total_spent': customer.total_spent,
        'total_orders': customer.total_orders,
        'loyalty_member': customer.loyalty_member
    }, 200

@customers_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_customer_profile():
    """Update customer profile"""
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(user_id=user_id).first()
    
    if not customer:
        return {'error': 'Customer profile not found'}, 404
    
    data = request.get_json()
    customer.phone = data.get('phone', customer.phone)
    customer.address = data.get('address', customer.address)
    customer.city = data.get('city', customer.city)
    customer.postal_code = data.get('postal_code', customer.postal_code)
    customer.country = data.get('country', customer.country)
    customer.notes = data.get('notes', customer.notes)
    
    db.session.commit()
    
    return {'message': 'Profile updated successfully'}, 200

@customers_bp.route('/photos', methods=['GET'])
def get_customer_photos():
    """Get all customer photos (day-to-day feature)"""
    featured_only = request.args.get('featured_only', 'false').lower() == 'true'
    limit = request.args.get('limit', 20, type=int)
    
    query = CustomerPhoto.query.order_by(CustomerPhoto.created_at.desc())
    
    if featured_only:
        query = query.filter_by(is_featured=True)
    
    photos = query.limit(limit).all()
    
    return {
        'photos': [{
            'id': p.id,
            'customer_id': p.customer_id,
            'photo_url': p.photo_url,
            'caption': p.caption,
            'product_purchased': p.product_purchased,
            'is_featured': p.is_featured,
            'likes': p.likes,
            'comments_count': p.comments_count,
            'taken_at': p.taken_at.isoformat()
        } for p in photos]
    }, 200

@customers_bp.route('/photos', methods=['POST'])
@jwt_required()
def upload_customer_photo():
    """Upload customer photo"""
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(user_id=user_id).first()
    
    if not customer:
        return {'error': 'Customer profile not found'}, 404
    
    data = request.get_json()
    
    photo = CustomerPhoto(
        customer_id=customer.id,
        photo_url=data.get('photo_url'),
        caption=data.get('caption'),
        product_purchased=data.get('product_purchased')
    )
    
    db.session.add(photo)
    db.session.commit()
    
    return {
        'id': photo.id,
        'message': 'Photo uploaded successfully'
    }, 201

@customers_bp.route('/photos/<int:photo_id>/like', methods=['POST'])
def like_photo(photo_id):
    """Like a customer photo"""
    photo = CustomerPhoto.query.get(photo_id)
    
    if not photo:
        return {'error': 'Photo not found'}, 404
    
    photo.likes += 1
    db.session.commit()
    
    return {'message': 'Photo liked successfully', 'likes': photo.likes}, 200

@customers_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get customer details (admin)"""
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return {'error': 'Customer not found'}, 404
    
    return {
        'id': customer.id,
        'user_id': customer.user_id,
        'phone': customer.phone,
        'address': customer.address,
        'city': customer.city,
        'postal_code': customer.postal_code,
        'country': customer.country,
        'total_spent': customer.total_spent,
        'total_orders': customer.total_orders,
        'last_order_date': customer.last_order_date.isoformat() if customer.last_order_date else None,
        'loyalty_member': customer.loyalty_member
    }, 200
