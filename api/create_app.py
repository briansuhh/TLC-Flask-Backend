from flask import Flask, request, jsonify
from flask_cors import CORS
from .middleware import jwt_required
from .config import Config
from .extensions import db, migrate, api, ma, jwt
from .routes import index_blueprint, auth_blueprint, product_blueprint, supplier_blueprint, branch_blueprint, tag_blueprint, category_blueprint, recipe_blueprint, inventory_item_blueprint, outlet_blueprint, branch_stock_count_blueprint
from .seeds.products import register_commands as register_products
from .seeds.outlets import register_commands as register_outlets
from .seeds.suppliers import register_commands as register_suppliers
from .seeds.recipes import register_commands as register_recipes
from .seeds.inventoryitems import register_commands as register_inventory_items
from .seeds.branches import register_commands as register_branches
from .seeds.branchstockcounts import register_commands as register_branch_stock_counts
from .seeds.categories import register_commands as register_categories
from .seeds.tags import register_commands as register_tags
from .seeds.users import register_commands as register_users

def create_app():
    app = Flask(__name__)
    # Enable CORS for all domains on all routes (not recommended for production)
    CORS(app)

    # Or enable CORS for specific domains only (recommended for production)
    # CORS(app, resources={r"/*": {"origins": ["https://flutter-frontend.example.com", "https://angular-frontend.example.com"]}})
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    # @app.before_request
    # def check_authentication():
    #     unprotected_endpoints = ["/auth/login"]
    #     if request.path not in unprotected_endpoints: 
    #         jwt_required(request)
        
        
    register_products(app)
    register_outlets(app)
    register_suppliers(app)
    register_recipes(app)
    register_inventory_items(app)
    register_branches(app)
    register_branch_stock_counts(app)
    register_categories(app)
    register_tags(app)
    register_users(app)
    
    api.register_blueprint(index_blueprint)
    api.register_blueprint(product_blueprint)
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(supplier_blueprint)
    api.register_blueprint(category_blueprint)
    api.register_blueprint(branch_blueprint)
    api.register_blueprint(tag_blueprint)
    api.register_blueprint(recipe_blueprint)
    api.register_blueprint(inventory_item_blueprint)
    api.register_blueprint(outlet_blueprint)
    api.register_blueprint(branch_stock_count_blueprint)
    
    return app
