import os
from flask import Flask
from app.config import Config
from app.models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
