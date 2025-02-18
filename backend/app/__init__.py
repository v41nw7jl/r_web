# backend/app/__init__.py

from flask import Flask, jsonify  # jsonify is good to have
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api  # Make sure this is present!
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    # --- CRUCIAL: Blueprint Registration ---
    from .routes.auth_routes import auth_bp
    from .routes.task_routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # --- Root Route (Keep for now) ---
    @app.route('/')
    def home():
        print("--- Root route ('/') called ---")  # Keep this for now
        return "Welcome to the Flask Application!"

    return app