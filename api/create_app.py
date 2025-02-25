from flask import Flask
from .config import Config
from .extensions import db, migrate, api, ma, jwt
from .routes import index_blueprint, auth_blueprint
from .middleware import log_request

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)
    api.init_app(app)
    
    app.before_request(log_request)

    api.register_blueprint(index_blueprint)
    api.register_blueprint(auth_blueprint)  
    
    return app
