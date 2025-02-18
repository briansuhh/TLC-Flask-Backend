from flask import jsonify
from flask_smorest import Blueprint

index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def index():
    """
    Index route to test if server is running
    """
    return jsonify({"message": "Hello, Flask!"})
