# backend/app/__init__.py

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api  # Import Api
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

    # Initialize the Api object *with the app instance*
    api = Api(app)  # THIS IS THE KEY CHANGE

    # Import and register blueprints
    from .routes.auth_routes import auth_bp
    from .routes.task_routes import task_bp

    # Register blueprints directly with the app
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # --- Root Route (Keep for now) ---
    @app.route('/')
    def home():
        print("--- Root route ('/') called ---")
        return "Welcome to the Flask Application!"

    # --- TEMPORARY TEST CODE - Add this before 'return app' ---
    @app.route('/test_internal')
    def test_internal():
        import requests  # Import the requests library

        try:
            # Make a request to your own registration endpoint
            url = "http://127.0.0.1:5000/api/auth/register"  # Use localhost *within* the app
            headers = {'Content-Type': 'application/json'}
            data = {
                "username": "internaltest",
                "email": "internal@example.com",
                "password": "internalpassword",
                "reminder_preference": "1 hour",
                "name": "Internal Test"
            }
            response = requests.post(url, headers=headers, json=data)  # Use 'json=' for data

            print("--- Internal Request Status Code:", response.status_code)
            print("--- Internal Request Response:", response.text)

            return f"Internal Test - Status Code: {response.status_code}, Response: {response.text}", 200
        except Exception as e:
            return f"Internal Test Failed: {e}", 500

    # --- END OF TEMPORARY TEST CODE ---

    return app
