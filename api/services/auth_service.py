import jwt
from api.extensions import db
from api.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, UTC
from flask import current_app

class AuthService:
    @staticmethod
    def register_user(username, email, password):
        password_hash = generate_password_hash(password)
        
        new_user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        db.session.add(new_user)
        db.session.commit()
        
        return new_user

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def create_access_token(identity, expires_delta=None):
        """
        Create a JWT token using PyJWT.
        """
        payload = {
            "identity": identity,
            "exp": datetime.now(UTC) + expires_delta if expires_delta else datetime.now(UTC) + timedelta(hours=1)
        }
        
        return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def decode_access_token(token):
        """
        Decode a JWT token using PyJWT.
        """
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
