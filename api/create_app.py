from flask import Flask
from .config import Config
from .extensions import db, migrate, api, ma, jwt
from .routes import index_blueprint, auth_blueprint, product_blueprint, supplier_blueprint, category_blueprint
from .routes import index_blueprint, auth_blueprint, product_blueprint, supplier_blueprint, branch_blueprint, tag_blueprint
from .seeds import register_commands

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    
    register_commands(app)

    api.register_blueprint(index_blueprint)
    api.register_blueprint(product_blueprint)
    api.register_blueprint(auth_blueprint)
    api.register_blueprint(supplier_blueprint)
    api.register_blueprint(category_blueprint)
    api.register_blueprint(branch_blueprint)
    api.register_blueprint(tag_blueprint)
    
    return app
