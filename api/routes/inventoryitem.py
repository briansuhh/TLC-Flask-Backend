from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.inventoryitem_service import InventoryItemService 
from api.schemas.inventoryitems import InventorySchema  
from sqlalchemy.exc import IntegrityError
from api.middleware import jwt_required

# Define Blueprint for Inventory Items
inventory_item_blueprint = Blueprint('inventory_item', __name__, url_prefix="/inventory-items")

@inventory_item_blueprint.route('/', methods=['POST'])
@jwt_required
def create_inventory_item():
    inventory_item_schema = InventorySchema()  # Use InventorySchema for validation
    try:
        data = inventory_item_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    try:
        # Call the InventoryItemService to create the inventory item
        inventory_item = InventoryItemService.create_inventory_item(
            data['name'],
            data['cost'],
            data['unit'],
            data['stock_warning_level'],
            data['supplier_id']
        )
    except IntegrityError:
        return jsonify({"message": "Inventory item with this name already exists"}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': f'Inventory item {inventory_item.name} created successfully'}), 201

@inventory_item_blueprint.route('/<int:item_id>', methods=['GET'])
@jwt_required
def get_inventory_item(item_id):
    inventory_item = InventoryItemService.get_inventory_item_by_id(item_id)
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404
    inventory_item_schema = InventorySchema()
    return jsonify(inventory_item_schema.dump(inventory_item)), 200

@inventory_item_blueprint.route('/', methods=['GET'])
@jwt_required
def get_all_inventory_items():
    inventory_items = InventoryItemService.get_all_inventory_items()
    inventory_item_schema = InventorySchema(many=True)
    return jsonify(inventory_item_schema.dump(inventory_items)), 200

@inventory_item_blueprint.route('/<int:item_id>', methods=['PUT'])
@jwt_required
def update_inventory_item(item_id):
    inventory_item_schema = InventorySchema(partial=True)
    try:
        data = inventory_item_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    inventory_item = InventoryItemService.update_inventory_item(item_id, data)
    if not inventory_item:
        return jsonify({'error': 'Inventory item not found'}), 404
    return jsonify({'message': f'Inventory item {inventory_item.name} updated successfully'}), 200

@inventory_item_blueprint.route('/<int:item_id>', methods=['DELETE'])
@jwt_required
def delete_inventory_item(item_id):
    success = InventoryItemService.delete_inventory_item(item_id)
    if not success:
        return jsonify({'error': 'Inventory item not found'}), 404
    return jsonify({'message': 'Inventory item deleted successfully'}), 200
