from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from config import Config
from flask_migrate import Migrate  # Add this import

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    
    migrate = Migrate(app, db)  # Initialize Migrate after app is defined

    api = Api(app)

    from .routes.auth_routes import auth_bp
    from .routes.task_routes import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    @app.route('/')
    def home():
        return "Welcome to the Flask Application!"
    
    return app