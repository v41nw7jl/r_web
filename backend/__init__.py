from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-uri'
db = SQLAlchemy(app)

from backend.app import models
from backend.app.routes import auth_routes, task_routes