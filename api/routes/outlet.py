from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.outlet_service import OutletService
from api.schemas.outlets import OutletSchema
from sqlalchemy.exc import IntegrityError

outlet_blueprint = Blueprint('outlet', __name__, url_prefix="/outlets")

@outlet_blueprint.route('/', methods=['POST'])
def create_outlet():
    outlet_schema = OutletSchema()
    try:
        data = outlet_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    try:
        outlet = OutletService.create_outlet(
            data['product_id'],
            data['name'],
            data['price']
        )
    except IntegrityError:
        return jsonify({"message": "Outlet with this name already exists"}), 409
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': f'Outlet {outlet.name} created successfully'}), 201

@outlet_blueprint.route('/<int:outlet_id>', methods=['GET'])
def get_outlet(outlet_id):
    outlet = OutletService.get_outlet_by_id(outlet_id)
    if not outlet:
        return jsonify({'error': 'Outlet not found'}), 404
    outlet_schema = OutletSchema()
    return jsonify(outlet_schema.dump(outlet)), 200

@outlet_blueprint.route('/', methods=['GET'])
def get_all_outlets():
    outlets = OutletService.get_all_outlets()
    return jsonify(outlets), 200

@outlet_blueprint.route('/<int:outlet_id>', methods=['PUT'])
def update_outlet(outlet_id):
    outlet_schema = OutletSchema(partial=True)
    try:
        data = outlet_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
    outlet = OutletService.update_outlet(outlet_id, data)
    if not outlet:
        return jsonify({'error': 'Outlet not found'}), 404
    return jsonify({'message': f'Outlet {outlet.name} updated successfully'}), 200

@outlet_blueprint.route('/<int:outlet_id>', methods=['DELETE'])
def delete_outlet(outlet_id):
    success = OutletService.delete_outlet(outlet_id)
    if not success:
        return jsonify({'error': 'Outlet not found'}), 404
    return jsonify({'message': 'Outlet deleted successfully'}), 200
