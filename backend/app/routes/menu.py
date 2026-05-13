from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Product, User
from app.routes import menu_bp

def admin_required(f):
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated

@menu_bp.route('', methods=['GET'])
def get_menu():
    """Get all menu items"""
    category = request.args.get('category')
    featured_only = request.args.get('featured_only', 'false').lower() == 'true'
    
    query = Product.query
    
    if category:
        query = query.filter_by(category=category)
    
    if featured_only:
        query = query.filter_by(is_featured=True)
    
    products = query.filter_by(is_available=True).all()
    
    return {
        'products': [{
            'id': p.id,
            'name': p.name,
            'description': p.description,
            'category': p.category,
            'price': p.price,
            'image_url': p.image_url,
            'preparation_time': p.preparation_time
        } for p in products]
    }, 200

@menu_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product details"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'category': product.category,
        'price': product.price,
        'image_url': product.image_url,
        'preparation_time': product.preparation_time
    }, 200

@menu_bp.route('', methods=['POST'])
@admin_required
def create_product():
    """Create new menu item (admin only)"""
    data = request.get_json()
    
    product = Product(
        name=data.get('name'),
        description=data.get('description'),
        category=data.get('category'),
        price=data.get('price'),
        cost=data.get('cost'),
        image_url=data.get('image_url'),
        preparation_time=data.get('preparation_time')
    )
    
    db.session.add(product)
    db.session.commit()
    
    return {
        'id': product.id,
        'name': product.name,
        'message': 'Product created successfully'
    }, 201

@menu_bp.route('/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    """Update menu item (admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.category = data.get('category', product.category)
    product.price = data.get('price', product.price)
    product.cost = data.get('cost', product.cost)
    product.image_url = data.get('image_url', product.image_url)
    product.is_featured = data.get('is_featured', product.is_featured)
    product.preparation_time = data.get('preparation_time', product.preparation_time)
    
    db.session.commit()
    
    return {'message': 'Product updated successfully'}, 200

@menu_bp.route('/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    """Delete menu item (admin only)"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    db.session.delete(product)
    db.session.commit()
    
    return {'message': 'Product deleted successfully'}, 200
