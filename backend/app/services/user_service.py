# backend/app/services/user_service.py
from app import db
from app.models import User, UserProfile
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app
class UserService:
    @staticmethod
    def register_user(username, email, password, name, reminder_preference):
        if User.query.filter_by(username=username).first():
            raise ValueError('Username already exists')
        if User.query.filter_by(email=email).first():
            raise ValueError('Email already exists')

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.flush() # Get the user ID before committing

        profile = UserProfile(user_id=user.id, name=name, reminder_preference=reminder_preference)
        db.session.add(profile)

        db.session.commit()
        return user

    @staticmethod
    def authenticate_user(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def reset_password(token, new_password):
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            email = serializer.loads(token, salt='password-reset-salt', max_age=3600)
        except SignatureExpired:
            raise ValueError('Token has expired')
        except BadSignature:
            raise ValueError('Invalid token')
        user = UserService.get_user_by_email(email)  # Use the service method
        if not user:
            raise ValueError('User not found')
        user.set_password(new_password)  # Use set_password to hash
        db.session.commit()