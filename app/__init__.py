from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import Config
from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes import auth_bp, user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "User Management API"
        },
    )

    app.register_blueprint(swaggerui_blueprint)

    return app