from api.extensions import db
from api.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token

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
    def create_access_token(identity):
        """
        Create a JWT token using Flask-JWT-Extended.
        """
        return create_access_token(identity=identity)
    
    @staticmethod
    def decode_access_token(token):
        """
        Decode a JWT token using Flask-JWT-Extended.
        """
        try:
            payload = decode_token(token)
            return payload
        except Exception:
            return None
