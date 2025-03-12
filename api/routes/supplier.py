from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.supplier_service import SupplierService
from api.schemas.suppliers import SupplierSchema
from sqlalchemy.exc import IntegrityError

supplier_blueprint = Blueprint('supplier', __name__, url_prefix="/suppliers")


@supplier_blueprint.route('/', methods=['POST'])
def create_supplier():
    supplier_schema = SupplierSchema()

    try:
        data = supplier_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        supplier = SupplierService.create_supplier(
            data['name'],
            data['email'],
            data['phone'],
            data['country_code']
        )
    except IntegrityError as e:
        if "suppliers.email" in str(e.orig):
            return jsonify({"message": "Supplier with this email already exists"}), 409
        if "suppliers.phone" in str(e.orig):
            return jsonify({"message": "Supplier with this phone number already exists"}), 409
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'Supplier {supplier.name} created successfully'}), 201


@supplier_blueprint.route('/<int:supplier_id>', methods=['GET'])
def get_supplier(supplier_id):
    supplier = SupplierService.get_supplier_by_id(supplier_id)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404

    supplier_schema = SupplierSchema()
    return jsonify(supplier_schema.dump(supplier)), 200


@supplier_blueprint.route('/', methods=['GET'])
def get_all_suppliers():
    suppliers = SupplierService.get_all_suppliers()
    supplier_schema = SupplierSchema(many=True)
    return jsonify(supplier_schema.dump(suppliers)), 200


@supplier_blueprint.route('/<int:supplier_id>', methods=['PUT'])
def update_supplier(supplier_id):
    supplier_schema = SupplierSchema(partial=True)

    try:
        data = supplier_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    supplier = SupplierService.update_supplier(supplier_id, data)
    if not supplier:
        return jsonify({'error': 'Supplier not found'}), 404

    return jsonify({'message': f'Supplier {supplier.name} updated successfully'}), 200


@supplier_blueprint.route('/<int:supplier_id>', methods=['DELETE'])
def delete_supplier(supplier_id):
    success = SupplierService.delete_supplier(supplier_id)
    if not success:
        return jsonify({'error': 'Supplier not found'}), 404

    return jsonify({'message': 'Supplier deleted successfully'}), 200
