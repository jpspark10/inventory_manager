import os
from flask import Flask
from .extensions import db, login_manager, migrate
from .api import api_bp
from .web import web_bp
from .auth import auth_bp


def create_app():
    app = Flask(__name__)
    # Load config from environment or defaults
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'sqlite:///inventory.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # Create tables if they do not exist
    with app.app_context():
        db.create_all()

    return app