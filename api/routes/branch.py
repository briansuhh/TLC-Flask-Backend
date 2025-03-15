from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.branch_service import BranchService
from api.schemas.branches import BranchSchema
from sqlalchemy.exc import IntegrityError

branch_blueprint = Blueprint('branch', __name__, url_prefix="/branches")


@branch_blueprint.route('/', methods=['POST'])
def create_branch():
    branch_schema = BranchSchema()

    try:
        data = branch_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        branch = BranchService.create_branch(
            data['name'],
            data['address']
        )
    except IntegrityError as e:
        if "branches.name" in str(e.orig):
            return jsonify({"message": "Branch with this name already exists"}), 409
        if "branches.address" in str(e.orig):
            return jsonify({"message": "Branch with this address already exists"}), 409
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': f'Branch {branch.name} created successfully'}), 201


@branch_blueprint.route('/<int:branch_id>', methods=['GET'])
def get_branch(branch_id):
    branch = BranchService.get_branch_by_id(branch_id)
    if not branch:
        return jsonify({'error': 'Branch not found'}), 404

    branch_schema = BranchSchema()
    return jsonify(branch_schema.dump(branch)), 200


@branch_blueprint.route('/', methods=['GET'])
def get_all_branch():
    branches = BranchService.get_all_branches()
    branch_schema = BranchSchema(many=True)
    return jsonify(branch_schema.dump(branches)), 200


@branch_blueprint.route('/<int:branch_id>', methods=['PUT'])
def update_branch(branch_id):
    branch_schema = BranchSchema(partial=True)

    try:
        data = branch_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    branch = BranchService.update_branch(branch_id, data)
    if not branch:
        return jsonify({'error': 'Branch not found'}), 404

    return jsonify({'message': f'Branch {branch.name} updated successfully'}), 200


@branch_blueprint.route('/<int:branch_id>', methods=['DELETE'])
def delete_branch(branch_id):
    success = BranchService.delete_branch(branch_id)
    if not success:
        return jsonify({'error': 'Branch not found'}), 404

    return jsonify({'message': 'Branch deleted successfully'}), 200
