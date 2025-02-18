from flask import jsonify
from flask_smorest import Blueprint

# Create a Blueprint for modular routes
index_blueprint = Blueprint('index', __name__)

@index_blueprint.route('/')
def index():
    """
    Index route to test if server is running
    """
    return jsonify({"message": "Hello, Flask!"})
