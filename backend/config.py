# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # MUST be before accessing os.environ
print("--- .env File Loaded (if this prints, load_dotenv() ran) ---")
print(f"DATABASE_URI from os.environ.get: {os.environ.get('DATABASE_URI')}")
print(f"DATABASE_URI from os.environ (raw): {os.environ}") # added to check all env variables

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Flask-Mail Configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    PASSWORD_RESET_BASE = os.environ.get('PASSWORD_RESET_BASE')