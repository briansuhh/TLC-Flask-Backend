from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.auth_service import AuthService
from api.schemas.users import UserSchema, UserLoginSchema
from datetime import timedelta
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

auth_blueprint = Blueprint('auth', __name__, url_prefix="/auth")

@auth_blueprint.route('/register', methods=['POST'])
def register():
    # Validate and deserialize input data
    user_schema = UserSchema()
    try:
        data = user_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Call the service to register the user
    try:
        user = AuthService.register_user(
            data['username'],
            data['email'],
            data['password']
        )
    except (UniqueViolation, IntegrityError) as e:
        return jsonify({"message": "That username already exists"}), 409
    except Exception as e:
        print(type(e))
        return jsonify({'error': str(e)}), 500

    # Return a success message
    return jsonify({'message': f'User {user.username} registered successfully'}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    # Validate and deserialize input data
    login_schema = UserLoginSchema()
    try:
        data = login_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # Authenticate user
    user = AuthService.authenticate_user(data['username'], data['password'])

    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Create JWT token using PyJWT
    access_token = AuthService.create_access_token(identity=user.username, expires_delta=timedelta(hours=1))

    return jsonify({'access_token': access_token}), 200
