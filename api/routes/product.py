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


@product_blueprint.route('/<int:product_id>/tags/', methods=['POST'])
def add_tag_to_product(product_id):
    """Attach an existing tag to a product"""
    data = request.get_json()
    tag_id = data.get('tag_id')

    if not tag_id:
        return jsonify({"error": "Tag ID is required"}), 400

    try:
        success = ProductService.add_tag_to_product(product_id, tag_id)
        if not success:
            return jsonify({'error': 'Product or Tag not found'}), 404

        return jsonify({'message': f'Tag {tag_id} added to product {product_id}'}), 201
    except IntegrityError:
        return jsonify({"message": "Tag is already associated with the product"}), 409


@product_blueprint.route('/<int:product_id>/tags/', methods=['GET'])
def get_product_tags(product_id):
    """Get all tags associated with a product"""
    product = ProductService.get_product_by_id(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    tags = ProductService.get_product_tags(product_id)
    return jsonify(tags), 200

@product_blueprint.route('/<int:product_id>/tags/<int:tag_id>', methods=['PUT'])
def update_product_tag(product_id, tag_id):
    """Update a tag associated with a product"""
    data = request.get_json()
    success = ProductService.update_product_tag(product_id, tag_id, data)
    if not success:
        return jsonify({'error': 'Product or Tag not found'}), 404

    return jsonify({'message': f'Tag {tag_id} updated for product {product_id}'}), 200

@product_blueprint.route('/<int:product_id>/tags/<int:tag_id>', methods=['DELETE'])
def remove_tag_from_product(product_id, tag_id):
    """Remove a tag from a product"""
    success = ProductService.remove_tag_from_product(product_id, tag_id)
    if not success:
        return jsonify({'error': 'Product or Tag not found'}), 404

    return jsonify({'message': f'Tag {tag_id} removed from product {product_id}'}), 200

