from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.category_service import CategoryService
from api.schemas.categories import CategorySchema
from sqlalchemy.exc import IntegrityError
from api.middleware import jwt_required

category_blueprint = Blueprint('category', __name__, url_prefix="/categories")

@category_blueprint.route('/', methods=['POST'])
@jwt_required
def create_category():
    category_schema = CategorySchema()

    try:
        data = category_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        category = CategoryService.create_category(
            data['name']
        )
    except IntegrityError as e:
        if "categories.name" in str(e.orig):
            return jsonify({"message": "Category with this name already exists"}), 409
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'Category {category.name} created successfully'}), 201

@category_blueprint.route('/<int:category_id>', methods=['GET'])
@jwt_required
def get_category(category_id):
    category = CategoryService.get_category_by_id(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    category_schema = CategorySchema()
    return jsonify(category_schema.dump(category)), 200

@category_blueprint.route('/', methods=['GET'])
@jwt_required
def get_all_categories():
    categories = CategoryService.get_all_categories()
    category_schema = CategorySchema(many=True)
    return jsonify(category_schema.dump(categories)), 200

@category_blueprint.route('/<int:category_id>', methods=['PUT'])
@jwt_required
def update_category(category_id):
    category_schema = CategorySchema(partial=True)

    try:
        data = category_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    category = CategoryService.update_category(category_id, data)
    if not category:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': f'Category {category.name} updated successfully'}), 200

@category_blueprint.route('/<int:category_id>', methods=['DELETE'])
@jwt_required
def delete_category(category_id):
    result = CategoryService.delete_category(category_id)
    if not result:
        return jsonify({'error': 'Category not found'}), 404

    return jsonify({'message': 'Category deleted successfully'}), 200

