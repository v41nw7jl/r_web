# backend/app/routes/auth_routes.py

from flask import request, jsonify, Blueprint
from flask_restful import Resource, Api, reqparse
from app import db, bcrypt
from app.models import User, UserProfile
from app.auth import authenticate, generate_token
from app.services.user_service import UserService
from app.utils.email import send_password_reset_email

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
api = Api(auth_bp)

# --- Argument Parsers ---
register_parser = reqparse.RequestParser()
register_parser.add_argument('username', type=str, required=True, help='Username is required')
register_parser.add_argument('email', type=str, required=True, help='Email is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')
register_parser.add_argument('name', type=str, required=False)
register_parser.add_argument('reminder_preference', type=str, required=True, help='Reminder preference is required')

login_parser = reqparse.RequestParser()
login_parser.add_argument('username', type=str, required=True, help='Username is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

reset_request_parser = reqparse.RequestParser()
reset_request_parser.add_argument('email', type=str, required=True, help='Email is required')

reset_password_parser = reqparse.RequestParser()
reset_password_parser.add_argument('token', type=str, required=True, help='Token is required')
reset_password_parser.add_argument('new_password', type=str, required=True, help='New password is required')


# --- Resource Classes ---
class UserRegistration(Resource):
    def post(self):
        print("--- UserRegistration.post() called ---")  # Add this
        args = register_parser.parse_args()
        print(f"--- Parsed arguments: {args} ---")  # Add this
        try:
            user = UserService.register_user(
                args['username'], args['email'], args['password'],
                args.get('name', ''), args['reminder_preference'] # get vs []
            )
            print(f"--- User created: {user} ---")  # Add this
            return {'message': 'User registered successfully', 'user_id': user.id}, 201
        except ValueError as e:
            print(f"--- ValueError: {e} ---")  # Add this
            return {'message': str(e)}, 400
        except Exception as e: # catch other errors
            print(f"--- Exception: {e} ---")
            return {'message': 'An error occurred' + str(e)}, 500

class UserLogin(Resource):
    def post(self):
        print("--- UserLogin.post() called ---") # Add this
        args = login_parser.parse_args()
        print(f"--- Parsed arguments (Login): {args} ---") # Add this
        user = UserService.authenticate_user(args['username'], args['password'])
        if user:
            token = generate_token(user.id)
            print(f"---- Token Generated: {token}") # Add this
            return {'message': 'Login successful', 'token': token}, 200
        else:
            print("--- Login failed ---")  # Add this
            return {'message': 'Invalid username or password'}, 401

class UserLogout(Resource):
    @authenticate  # Apply the authentication decorator
    def post(self, user):
        print("--- UserLogout.post() called ---")  # Add this
        # JWTs are stateless, so "logout" is handled client-side by discarding the token.
        return {'message': 'Logout successful'}, 200

class PasswordResetRequest(Resource):
    def post(self):
        print("--- PasswordResetRequest.post() called ---")  # Add this
        args = reset_request_parser.parse_args()
        try:
            send_password_reset_email(args['email'])
            return {'message': 'If a matching email is found, a password reset email has been sent.'}, 200
        except ValueError as e:
             print(f"--- ValueError: {e} ---") # Add this
             return {'message': str(e)}, 400
        except Exception as e:
            print(f"--- Exception: {e} ---") # Add this
            return {'message': 'An error occurred while sending the email.'}, 500


class PasswordReset(Resource):
    def post(self):
        print("--- PasswordReset.post() called ---")  # Add this
        args = reset_password_parser.parse_args()
        try:
            UserService.reset_password(args['token'], args['new_password'])
            return {'message': 'Password has been reset successfully'}, 200
        except ValueError as e:
            print(f"--- ValueError: {e} ---") # Add this
            return {'message': str(e)}, 400
        except Exception as e:
            print(f"--- Exception: {e} ---")  # Add this
            return {'message':"Failed"}, 400

# --- Add resources to the API ---
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(PasswordResetRequest, '/reset_password_request')
api.add_resource(PasswordReset, '/reset_password')