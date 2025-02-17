# backend/app/auth.py
from functools import wraps
from flask import request, jsonify, current_app
from app.models import User
import jwt
from datetime import datetime, timedelta, timezone

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.now(timezone.utc) + timedelta(hours=24)  # Token expires in 24 hours
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing'}), 401

        try:
            auth_type, token = auth_header.split(" ")
            if auth_type.lower() != "bearer":
                raise ValueError("Invalid authorization type")
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload['user_id']
            user = User.query.get(user_id)  # Use query.get() for primary key lookup
            if not user:
                return jsonify({'message': 'User not found'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except (jwt.InvalidTokenError, ValueError):
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return func(user, *args, **kwargs)  # Pass the user object

    return wrapper