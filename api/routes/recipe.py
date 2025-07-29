from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.recipe_service import RecipeService 
from api.schemas.recipes import RecipeSchema 
from sqlalchemy.exc import IntegrityError
from api.middleware import jwt_required

recipe_blueprint = Blueprint('recipe', __name__, url_prefix="/recipes")

@recipe_blueprint.route('/', methods=['POST'])
@jwt_required
def create_recipe():
    recipe_schema = RecipeSchema()
    try:
        data = recipe_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    try:
        recipe = RecipeService.create_recipe(
            data['product_id'],
            data['item_id'],
            data['quantity'],
            data['isTakeout']
        )
    except IntegrityError:
        return jsonify({"message": "Recipe with this product_id and item_id already exists"}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': f'Recipe for Product {recipe.product_id} and Item {recipe.item_id} created successfully'}), 201

@recipe_blueprint.route('/<int:product_id>/<int:item_id>', methods=['GET'])
@jwt_required
def get_recipe(product_id, item_id):
    recipe = RecipeService.get_recipe_by_product_item(product_id, item_id)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    recipe_schema = RecipeSchema()
    return jsonify(recipe_schema.dump(recipe)), 200

@recipe_blueprint.route('/', methods=['GET'])
@jwt_required
def get_all_recipes():
    recipes = RecipeService.get_all_recipes()
    recipe_schema = RecipeSchema(many=True)
    return jsonify(recipe_schema.dump(recipes)), 200

@recipe_blueprint.route('/<int:product_id>/<int:item_id>', methods=['PUT'])
@jwt_required
def update_recipe(product_id, item_id):
    recipe_schema = RecipeSchema(partial=True)
    try:
        data = recipe_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    recipe = RecipeService.update_recipe(product_id, item_id, data)
    if not recipe:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify({'message': f'Recipe for Product {recipe.product_id} and Item {recipe.item_id} updated successfully'}), 200

@recipe_blueprint.route('/<int:product_id>/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_recipe(product_id, item_id):
    success = RecipeService.delete_recipe(product_id, item_id)
    if not success:
        return jsonify({'error': 'Recipe not found'}), 404
    return jsonify({'message': 'Recipe deleted successfully'}), 200
