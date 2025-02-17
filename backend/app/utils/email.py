# backend/app/utils/email.py
from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
import os #used to access env variables

def send_password_reset_email(user_email):
    """Sends a password reset email to the user."""
    user =  current_app.extensions['sqlalchemy'].db.session.query(current_app.extensions['sqlalchemy'].db.Model._decl_class_registry["User"]).filter_by(email=user_email).first()
    if not user:
        raise ValueError('No user found with that email address.')
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(user_email, salt='password-reset-salt')
    reset_link = f"{current_app.config['PASSWORD_RESET_BASE']}/reset-password/{token}"  # e.g., http://your-app.com/reset-password/TOKEN

    msg = Message(
        'Password Reset Request',
        recipients=[user_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = f'Click the following link to reset your password: {reset_link}\n\nIf you did not request a password reset, please ignore this email.'
    try:
        current_app.extensions['mail'].send(msg)  # Correct way to send with Flask-Mail
    except Exception as e: # always use generic Exception
        # Ideally, log the error properly (e.g., to a file or error tracking service)
        print(f"Error sending email: {e}")  # Log the error for debugging.
        raise  # Re-raise the exception to be handled by the caller.

#Ideally this should be different file, as this is not related email.
def send_reminder_email(to_email, subject, task_details):
    """Sends a task reminder email."""
    msg = Message(
        subject=f"Reminder: {subject}",
        recipients=[to_email],
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    msg.body = f"Dear user,\n\nThis is a reminder for your task:\n\n{task_details}\n\nBest regards,\nReminder App"
    try:
        current_app.extensions['mail'].send(msg)
    except Exception as e:
        print(f"Error sending reminder email: {e}")
        raise