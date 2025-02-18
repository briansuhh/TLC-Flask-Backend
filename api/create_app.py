from flask import Flask
from .config import Config
from .extensions import db, migrate, api, ma
from .routes import index_blueprint, auth_blueprint
from .middleware import log_request

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    app.config["API_TITLE"] = "My API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.before_request(log_request)
    api.init_app(app)

    api.register_blueprint(index_blueprint)
    api.register_blueprint(auth_blueprint)
    
    return app
