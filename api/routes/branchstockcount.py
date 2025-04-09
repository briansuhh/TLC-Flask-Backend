from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.branchstockcount_service import BranchStockCountService
from api.schemas.branchstockcount import BranchStockCountSchema
from sqlalchemy.exc import IntegrityError

branch_stock_count_blueprint = Blueprint('branch_stock_count', __name__, url_prefix="/branchstockcounts")

@branch_stock_count_blueprint.route('/', methods=['POST'])
def create_branch_stock_count():
    branch_stock_count_schema = BranchStockCountSchema()
    try:
        # Validate and load data
        data = branch_stock_count_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        # Attempt to create the branch stock count
        branch_stock_count = BranchStockCountService.create_branch_stock_count(
            data['branch_id'],
            data['item_id'],
            data['in_stock'],
            data['ordered_qty']
        )
    except IntegrityError as e:
        return jsonify({"message": str(e)}), 409 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify({'message': f'Branch Stock Count for Branch {branch_stock_count.branch_id} and Item {branch_stock_count.item_id} created successfully'}), 201

@branch_stock_count_blueprint.route('/<int:branch_id>/<int:item_id>', methods=['GET'])
def get_branch_stock_count(branch_id, item_id):
    branch_stock_count = BranchStockCountService.get_branch_stock_count_by_ids(branch_id, item_id)
    if not branch_stock_count:
        return jsonify({'error': 'Branch stock count not found'}), 404
    branch_stock_count_schema = BranchStockCountSchema()
    return jsonify(branch_stock_count_schema.dump(branch_stock_count)), 200

@branch_stock_count_blueprint.route('/', methods=['GET'])
def get_all_branch_stock_counts():
    branch_stock_counts = BranchStockCountService.get_all_branch_stock_counts()
    branch_stock_count_schema = BranchStockCountSchema(many=True)
    return jsonify(branch_stock_count_schema.dump(branch_stock_counts)), 200

@branch_stock_count_blueprint.route('/<int:branch_id>/<int:item_id>', methods=['PUT'])
def update_branch_stock_count(branch_id, item_id):
    branch_stock_count_schema = BranchStockCountSchema(partial=True)
    try:
        data = branch_stock_count_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    branch_stock_count = BranchStockCountService.update_branch_stock_count(branch_id, item_id, data)
    if not branch_stock_count:
        return jsonify({'error': 'Branch stock count not found'}), 404
    return jsonify({'message': f'Branch Stock Count for Branch {branch_stock_count.branch_id} and Item {branch_stock_count.item_id} updated successfully'}), 200

@branch_stock_count_blueprint.route('/<int:branch_id>/<int:item_id>', methods=['DELETE'])
def delete_branch_stock_count(branch_id, item_id):
    success = BranchStockCountService.delete_branch_stock_count(branch_id, item_id)
    if not success:
        return jsonify({'error': 'Branch stock count not found'}), 404
    return jsonify({'message': 'Branch stock count deleted successfully'}), 200
