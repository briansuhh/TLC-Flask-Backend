from flask import request, jsonify
from api.services.auth_service import AuthService

def jwt_required(f):
    """
    A decorator to require JWT verification for specific routes.
    """
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        try:
            payload = AuthService.decode_access_token(token)
            if payload is None:
                return jsonify({'error': 'Invalid or expired token'}), 401

            request.user_identity = payload['identity']
            return f(*args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return wrapper
