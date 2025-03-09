from api.extensions import db
from api.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, decode_token

class AuthService:
    @staticmethod
    def register_user(username, first_name, middle_name, last_name, birth_date, sex, position, email, password):
        password_hash = generate_password_hash(password)
        
        new_user = User(
            username=username,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            birth_date=birth_date,
            sex=sex,
            position=position,
            email=email,
            password_hash=password_hash,
        )

        db.session.add(new_user)
        db.session.commit()
        
        return new_user

    @staticmethod
    def authenticate_user(email, password):
        user = User.query.filter_by(email=email).first() 
        
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def create_access_token(identity):
        """
        Create a JWT token using Flask-JWT-Extended.
        """
        return create_access_token(
            identity=identity.id,
            additional_claims={
                "username": identity.username,
                "email": identity.email,
                "position": identity.position,
            }            
        )
    
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
