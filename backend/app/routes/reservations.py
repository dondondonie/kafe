from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date, time
from app import db
from app.models import Reservation, User
from app.routes import reservations_bp
import uuid

@reservations_bp.route('', methods=['GET'])
@jwt_required()
def get_reservations():
    """Get reservations"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role == 'admin':
        reservations = Reservation.query.all()
    else:
        reservations = Reservation.query.filter_by(user_id=user_id).all()
    
    return {
        'reservations': [{
            'id': r.id,
            'reservation_number': r.reservation_number,
            'guest_count': r.guest_count,
            'reservation_date': r.reservation_date.isoformat(),
            'status': r.status,
            'payment_status': r.payment_status,
            'deposit_amount': r.deposit_amount,
            'total_amount': r.total_amount
        } for r in reservations]
    }, 200

@reservations_bp.route('', methods=['POST'])
@jwt_required()
def create_reservation():
    """Create new reservation with payment requirement"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    reservation = Reservation(
        user_id=user_id,
        reservation_number=f"RES-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}",
        guest_count=data.get('guest_count'),
        reservation_date=datetime.fromisoformat(data.get('reservation_date')),
        reservation_time=datetime.strptime(data.get('reservation_time'), '%H:%M').time(),
        duration=data.get('duration', 60),
        special_requests=data.get('special_requests'),
        deposit_amount=data.get('deposit_amount', 0),
        total_amount=data.get('total_amount'),
        payment_method=data.get('payment_method', 'pending')
    )
    
    db.session.add(reservation)
    db.session.commit()
    
    return {
        'id': reservation.id,
        'reservation_number': reservation.reservation_number,
        'status': reservation.status,
        'payment_status': reservation.payment_status,
        'message': 'Reservation created successfully. Awaiting payment.'
    }, 201

@reservations_bp.route('/<int:reservation_id>', methods=['GET'])
@jwt_required()
def get_reservation(reservation_id):
    """Get reservation details"""
    reservation = Reservation.query.get(reservation_id)
    
    if not reservation:
        return {'error': 'Reservation not found'}, 404
    
    return {
        'id': reservation.id,
        'reservation_number': reservation.reservation_number,
        'guest_count': reservation.guest_count,
        'reservation_date': reservation.reservation_date.isoformat(),
        'reservation_time': reservation.reservation_time.isoformat(),
        'duration': reservation.duration,
        'status': reservation.status,
        'payment_status': reservation.payment_status,
        'payment_method': reservation.payment_method,
        'deposit_amount': reservation.deposit_amount,
        'total_amount': reservation.total_amount,
        'special_requests': reservation.special_requests,
        'created_at': reservation.created_at.isoformat()
    }, 200

@reservations_bp.route('/<int:reservation_id>/confirm', methods=['PUT'])
@jwt_required()
def confirm_reservation(reservation_id):
    """Confirm reservation after payment"""
    reservation = Reservation.query.get(reservation_id)
    
    if not reservation:
        return {'error': 'Reservation not found'}, 404
    
    if reservation.payment_status != 'paid':
        return {'error': 'Payment must be completed first'}, 400
    
    reservation.status = 'confirmed'
    reservation.confirmed_at = datetime.utcnow()
    
    db.session.commit()
    
    return {'message': 'Reservation confirmed successfully'}, 200

@reservations_bp.route('/<int:reservation_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_reservation(reservation_id):
    """Cancel reservation"""
    reservation = Reservation.query.get(reservation_id)
    
    if not reservation:
        return {'error': 'Reservation not found'}, 404
    
    if reservation.status == 'completed':
        return {'error': 'Cannot cancel completed reservation'}, 400
    
    reservation.status = 'cancelled'
    db.session.commit()
    
    return {'message': 'Reservation cancelled successfully'}, 200
