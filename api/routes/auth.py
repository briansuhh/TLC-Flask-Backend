from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.auth_service import AuthService
from api.schemas.users import UserSchema, UserLoginSchema
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

auth_blueprint = Blueprint('auth', __name__, url_prefix="/auth")

@auth_blueprint.route('/register', methods=['POST'])
def register():
    user_schema = UserSchema()
    try:
        data = user_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        user = AuthService.register_user(
            data['username'],
            data['first_name'],
            data['middle_name'],
            data['last_name'],
            data['birth_date'],
            data['sex'],
            data['position'],
            data['email'],
            data['password']
        )
    except (IntegrityError) as e:
        return jsonify({"message": "That email already exists"}), 409
    except Exception as e:
        print(type(e))
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'User {user.username} registered successfully'}), 201


@auth_blueprint.route('/login', methods=['POST'])
def login():
    login_schema = UserLoginSchema()
    try:
        data = login_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    user = AuthService.authenticate_user(data['email'], data['password'])

    print(user)

    if user is None:
        return jsonify({'error': 'Invalid credentials'}), 401

    access_token = AuthService.create_access_token(identity=user)

    return jsonify({'access_token': access_token}), 200
