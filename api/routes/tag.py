from flask import request, jsonify
from flask_smorest import Blueprint
from api.services.tag_service import TagService
from api.schemas.tags import TagSchema
from sqlalchemy.exc import IntegrityError
from api.middleware import jwt_required

tag_blueprint = Blueprint('tag', __name__, url_prefix="/tags")

@tag_blueprint.route('/', methods=['POST'])
@jwt_required
def create_tag():
    tag_schema = TagSchema()

    try:
        data = tag_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    try:
        tag = TagService.create_tag(
            data['name']
        )
    except IntegrityError as e:
        if "tags.name" in str(e.orig):
            return jsonify({"message": "Tag with this name already exists"}), 409
        return jsonify({'error': 'Database integrity error'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    return jsonify({'message': f'Tag {tag.name} created successfully'}), 201


@tag_blueprint.route('/<int:tag_id>', methods=['GET'])
@jwt_required
def get_tag(tag_id):
    tag = TagService.get_tag_by_id(tag_id)
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    tag_schema = TagSchema()
    return jsonify(tag_schema.dump(tag)), 200

@tag_blueprint.route('/', methods=['GET'])
@jwt_required
def get_all_tags():
    tags = TagService.get_all_tags()
    tag_schema = TagSchema(many=True)
    return jsonify(tag_schema.dump(tags)), 200

@tag_blueprint.route('/<int:tag_id>', methods=['PUT'])
@jwt_required
def update_tag(tag_id):
    tag_schema = TagSchema(partial=True)

    try:
        data = tag_schema.load(request.json)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    tag = TagService.update_tag(tag_id, data)
    if not tag:
        return jsonify({'error': 'Tag not found'}), 404

    return jsonify({'message': f'Tag {tag.name} updated successfully'}), 200

@tag_blueprint.route('/<int:tag_id>', methods=['DELETE'])
@jwt_required
def delete_tag(tag_id):
    result = TagService.delete_tag(tag_id)
    if not result:
        return jsonify({'error': 'Tag not found'}), 404

    return jsonify({'message': 'Tag deleted successfully'}), 200
