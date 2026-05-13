from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Inventory, Product, User
from app.routes import inventory_bp

def admin_required(f):
    @jwt_required()
    def decorated(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return {'error': 'Admin access required'}, 403
        return f(*args, **kwargs)
    return decorated

@inventory_bp.route('', methods=['GET'])
@jwt_required()
def get_inventory():
    """Get all inventory items"""
    low_stock_only = request.args.get('low_stock_only', 'false').lower() == 'true'
    
    query = Inventory.query.join(Product)
    
    if low_stock_only:
        query = query.filter(Inventory.quantity <= Inventory.reorder_level)
    
    inventories = query.all()
    
    return {
        'inventory': [{
            'id': inv.id,
            'product_id': inv.product_id,
            'product_name': inv.product.name,
            'quantity': inv.quantity,
            'unit': inv.unit,
            'min_stock': inv.min_stock,
            'max_stock': inv.max_stock,
            'reorder_level': inv.reorder_level,
            'is_low_stock': inv.is_low_stock(),
            'last_restock': inv.last_restock
        } for inv in inventories]
    }, 200

@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
@jwt_required()
def get_inventory_item(inventory_id):
    """Get inventory item details"""
    inventory = Inventory.query.get(inventory_id)
    
    if not inventory:
        return {'error': 'Inventory item not found'}, 404
    
    return {
        'id': inventory.id,
        'product_id': inventory.product_id,
        'product_name': inventory.product.name,
        'quantity': inventory.quantity,
        'unit': inventory.unit,
        'min_stock': inventory.min_stock,
        'max_stock': inventory.max_stock,
        'reorder_level': inventory.reorder_level,
        'is_low_stock': inventory.is_low_stock()
    }, 200

@inventory_bp.route('', methods=['POST'])
@admin_required
def create_inventory():
    """Create inventory item"""
    data = request.get_json()
    
    # Check if product exists
    product = Product.query.get(data.get('product_id'))
    if not product:
        return {'error': 'Product not found'}, 404
    
    # Check if inventory already exists
    existing = Inventory.query.filter_by(product_id=data.get('product_id')).first()
    if existing:
        return {'error': 'Inventory already exists for this product'}, 400
    
    inventory = Inventory(
        product_id=data.get('product_id'),
        quantity=data.get('quantity', 0),
        unit=data.get('unit', 'units'),
        min_stock=data.get('min_stock', 10),
        max_stock=data.get('max_stock', 100),
        reorder_level=data.get('reorder_level', 20)
    )
    
    db.session.add(inventory)
    db.session.commit()
    
    return {
        'id': inventory.id,
        'product_id': inventory.product_id,
        'message': 'Inventory item created successfully'
    }, 201

@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
@admin_required
def update_inventory(inventory_id):
    """Update inventory item"""
    inventory = Inventory.query.get(inventory_id)
    
    if not inventory:
        return {'error': 'Inventory item not found'}, 404
    
    data = request.get_json()
    inventory.quantity = data.get('quantity', inventory.quantity)
    inventory.unit = data.get('unit', inventory.unit)
    inventory.min_stock = data.get('min_stock', inventory.min_stock)
    inventory.max_stock = data.get('max_stock', inventory.max_stock)
    inventory.reorder_level = data.get('reorder_level', inventory.reorder_level)
    
    db.session.commit()
    
    return {'message': 'Inventory item updated successfully'}, 200
