from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.product_service import ProductService
from api.schemas.products import ProductSchema
from sqlalchemy.exc import IntegrityError

product_blueprint = Blueprint('product', __name__, url_prefix="/products")

@product_blueprint.route('/', methods=['POST'])
def create_product():
    product_schema = ProductSchema()
    try:
        data = product_schema.load(request.json)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    try:
        product = ProductService.create_product(
            data['name'],
            data['variant_group_id'],
            data['sku'],
            data['category_id']
        )
    except IntegrityError:
        return jsonify({"message": "Product with this SKU already exists"}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': f'Product {product.name} created successfully'}), 201

@product_blueprint.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product_schema = ProductSchema()
    return jsonify(product_schema.dump(product)), 200

@product_blueprint.route('/', methods=['GET'])
def get_all_products():
    products = ProductService.get_all_products()
    return jsonify(products), 200

@product_blueprint.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product_schema = ProductSchema(partial=True)
    try:
        data = product_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    product = ProductService.update_product(product_id, data)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': f'Product {product.name} updated successfully'}), 200

@product_blueprint.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    success = ProductService.delete_product(product_id)
    if not success:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': 'Product deleted successfully'}), 200
