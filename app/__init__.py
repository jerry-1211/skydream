import os
from flask import Flask, render_template
from .extensions import db, migrate, login_manager, csrf
from .config import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '관리자 로그인이 필요합니다.'
    csrf.init_app(app)

    # Import models so that user_loader and model metadata are registered
    from . import models  # noqa: F401

    # Register blueprints
    from .blueprints.public import public_bp
    from .blueprints.auth import auth_bp
    from .blueprints.admin import admin_bp
    from .blueprints.health import health_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(health_bp)

    # Register error handlers
    register_error_handlers(app)

    # Ensure upload directories exist
    upload_folder = app.config.get('UPLOAD_FOLDER', 'app/static/uploads')
    for subdir in ['originals', 'thumbnails', 'webp']:
        os.makedirs(os.path.join(upload_folder, subdir), exist_ok=True)

    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return render_template('public/error/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('public/error/500.html'), 500
