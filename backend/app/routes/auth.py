from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.routes import auth_bp
import requests

@auth_bp.route('/oauth/google', methods=['POST'])
def google_oauth():
    """OAuth login with Google"""
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return {'error': 'Token required'}, 400
    
    try:
        # Verify token with Google
        response = requests.get(
            f'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={token}'
        )
        google_data = response.json()
        
        if 'error' in google_data:
            return {'error': 'Invalid token'}, 401
        
        email = google_data.get('email')
        name = google_data.get('name', '').split()
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                username=email.split('@')[0],
                first_name=name[0] if name else '',
                last_name=name[1] if len(name) > 1 else '',
                oauth_provider='google',
                oauth_id=google_data.get('id')
            )
            db.session.add(user)
            db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role
            }
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

@auth_bp.route('/oauth/github', methods=['POST'])
def github_oauth():
    """OAuth login with GitHub"""
    data = request.get_json()
    code = data.get('code')
    
    if not code:
        return {'error': 'Code required'}, 400
    
    try:
        # Exchange code for token
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            json={
                'client_id': 'your_github_client_id',
                'client_secret': 'your_github_secret',
                'code': code
            },
            headers={'Accept': 'application/json'}
        )
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        # Get user info
        user_response = requests.get(
            'https://api.github.com/user',
            headers={'Authorization': f'token {access_token}'}
        )
        github_data = user_response.json()
        
        email = github_data.get('email')
        if not email:
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={'Authorization': f'token {access_token}'}
            )
            emails = email_response.json()
            email = next((e['email'] for e in emails if e['primary']), emails[0]['email'])
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                username=github_data.get('login'),
                first_name=github_data.get('name', '').split()[0] if github_data.get('name') else '',
                avatar_url=github_data.get('avatar_url'),
                oauth_provider='github',
                oauth_id=str(github_data.get('id'))
            )
            db.session.add(user)
            db.session.commit()
        
        access_token = create_access_token(identity=user.id)
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'role': user.role
            }
        }, 200
        
    except Exception as e:
        return {'error': str(e)}, 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return {
        'id': user.id,
        'email': user.email,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'avatar_url': user.avatar_url,
        'role': user.role
    }, 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout user"""
    return {'message': 'Logged out successfully'}, 200
