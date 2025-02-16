# Task Reminder Web Application - Project Design Document

**Version:** 1.0
**Date:** Feb 16, 2025
**Authors:** [Allan]

## 1. Introduction

This document outlines the design and development plan for a web-based task reminder application. The application aims to provide users with a simple and effective way to manage their tasks and receive timely reminders, helping them stay organized and productive.  This document focuses on the Minimum Viable Product (MVP), encompassing Phases 1.1 and 1.2 of the overall project vision.

## 2. Goals

*   Provide a user-friendly web application for creating, managing, and tracking tasks.
*   Enable users to set due dates and times for tasks.
*   Implement a reliable email-based reminder system.
*   Offer a secure and private user experience.
*   Build a foundation for future expansion and feature additions.

## 3. Scope (MVP - Phases 1.1 and 1.2)

The MVP will include the following features:

*   **User Authentication:**
    *   User registration with email and password.
    *   Secure user login.
    *   Password reset functionality.
*   **Task Management:**
    *   Create new tasks with a title, description, due date, and due time.
    *   Edit existing tasks.
    *   Delete tasks.
    *   View a list of tasks, sorted by due date (ascending).
    *   Mark tasks as complete.
*   **Reminder System:**
    *   Allow users to set a reminder time preference (e.g., 1 hour before, 1 day before).  This preference will be stored in the user's profile.
    *   Send email reminders to users at their specified reminder time before the task's due date/time.
*   **User Profile:**
    *   Store basic user information: name, email address, and reminder time preference.

**Out of Scope (for MVP):**  All features listed in later phases (recurring tasks, collaboration, calendar integration, advanced filtering/sorting, etc.) are explicitly out of scope for this MVP.

## 4. System Architecture

The application will follow a client-server architecture:

*   **Client (Frontend):**
    *   Technology: React, HTML, CSS, JavaScript
    *   Responsibilities:
        *   User interface rendering.
        *   User interaction handling.
        *   Making API requests to the backend.
        *   Client-side validation (in addition to server-side validation).
*   **Server (Backend):**
    *   Technology: Python (Flask framework)
    *   Responsibilities:
        *   Handling API requests from the client.
        *   Database interaction (CRUD operations).
        *   User authentication and authorization.
        *   Business logic (e.g., determining when to send reminders).
        *   Sending email reminders.
*   **Database:**
    *   Technology: PostgreSQL (preferred) or MySQL
    *   Responsibilities:
        *   Storing user data (users, profiles).
        *   Storing task data (tasks, due dates, reminder preferences).
*   **Email Service:**
    *   Technology: Mailgun, SendGrid, or Amazon SES (to be selected based on cost and ease of integration). A free tier will be used during development and testing.  Flask-Mail will be used to abstract the email sending.
* **Deployment**
    * Platform : PythonAnywhere

**Diagram:**
+-----------------+ HTTP Requests +-----------------+ Database Queries +-----------------+
| Client | <-----------------> | Backend | <-------------------> | Database |
| (React) | (API) | (Flask) | (ORM) | (PostgreSQL/MySQL)|
+-----------------+ +-----------------+ +-----------------+
^ |
| | Email Sending
| v
| +-----------------+
+-------------------------------->| Email Service |
| (Mailgun/SendGrid/|
| SES) |
+-----------------+


## 5. Data Model

The following database tables will be used:

*   **users:**
    *   `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    *   `username` (VARCHAR, UNIQUE, NOT NULL)
    *   `email` (VARCHAR, UNIQUE, NOT NULL)
    *   `password_hash` (VARCHAR, NOT NULL)  // Store hashed passwords, *never* plain text!
    *   `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

*   **user_profiles:**
    *   `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY referencing `users.id`, UNIQUE, NOT NULL)
    *   `name` (VARCHAR)
    *   `reminder_preference` (VARCHAR, NOT NULL) // e.g., "1 hour", "1 day" - represent as a string for simplicity in the MVP.  Could use an integer representing minutes later.
     *   `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

*   **tasks:**
    *   `id` (INT, PRIMARY KEY, AUTO_INCREMENT)
    *   `user_id` (INT, FOREIGN KEY referencing `users.id`, NOT NULL)
    *   `title` (VARCHAR, NOT NULL)
    *   `description` (TEXT)
    *   `due_date` (DATE, NOT NULL)
    *   `due_time` (TIME, NOT NULL)
    *   `is_complete` (BOOLEAN, DEFAULT FALSE)
    *   `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)
    *   `updated_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)

**Relationships:**

*   One-to-one relationship between `users` and `user_profiles`.
*   One-to-many relationship between `users` and `tasks` (one user can have multiple tasks).

## 6. API Endpoints (RESTful)

The following API endpoints will be implemented using Flask-RESTful (or Flask-RESTX):

| Method | Endpoint                | Description                                         | Request Body (Example)                                  | Response (Example - Success)                     |
| ------ | ----------------------- | --------------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------- |
| POST   | `/api/users/register`    | Register a new user.                               | `{ "username": "testuser", "email": "test@example.com", "password": "securepassword" }` | `{ "id": 1, "username": "testuser", "email": "test@example.com" }` |
| POST   | `/api/users/login`       | Log in an existing user.                            | `{ "username": "testuser", "password": "securepassword" }` | `{ "message": "Login successful", "token": "JWT_TOKEN"}`  (See Authentication below) |
| POST   | `/api/users/logout`       | Log in an existing user.                            | `{ "token": "JWT_TOKEN" }` | `{ "message": "Logout successful" }` |
| GET    | `/api/users/reset_password`    | Request Password Reset                              | `{  "email": "test@example.com" }` | `{ "message": "Password reset mail has been sent."}`|
| POST    | `/api/users/reset_password`    | Submit New Password via token received in mail    | `{  "email": "test@example.com", "token" : "token_received", "new_password" : "new_password" }` | `{ "message": "Password has been reset."}`|
| GET    | `/api/tasks`             | Get all tasks for the logged-in user.                |  *(Requires authentication)*                             | `[ { "id": 1, "title": "Grocery Shopping", "due_date": "2023-10-28", "due_time": "10:00:00", "is_complete": false }, ... ]` |
| POST   | `/api/tasks`             | Create a new task.                                   | *(Requires authentication)* `{ "title": "Grocery Shopping", "description": "Buy milk, eggs, bread", "due_date": "2023-10-28", "due_time": "10:00:00" }` | `{ "id": 1, "title": "Grocery Shopping", ... }`      |
| GET    | `/api/tasks/<int:task_id>` | Get a specific task by ID.                          | *(Requires authentication)*                             | `{ "id": 1, "title": "Grocery Shopping", ... }`      |
| PUT    | `/api/tasks/<int:task_id>` | Update an existing task.                            | *(Requires authentication)* `{ "title": "Updated Task", "is_complete": true }` | `{ "id": 1, "title": "Updated Task", ... }`        |
| DELETE | `/api/tasks/<int:task_id>` | Delete a task.                                       | *(Requires authentication)*                             | `{ "message": "Task deleted successfully" }`        |
| PATCH   | `/api/tasks/<int:task_id>/complete` | Mark a task as complete.      | *(Requires authentication)*  `{}`          | `[ { "id": 1, "title": "Grocery Shopping", "due_date": "2023-10-28", "due_time": "10:00:00", "is_complete": true }, ... ]` |

**Authentication:**

*   JWT (JSON Web Tokens) will be used for authentication.
*   After successful login, a JWT will be returned to the client.
*   The client must include the JWT in the `Authorization` header (as a Bearer token) for all subsequent requests that require authentication.  Example: `Authorization: Bearer <JWT_TOKEN>`

**Error Handling:**

*   Appropriate HTTP status codes will be used to indicate errors (e.g., 400 Bad Request, 401 Unauthorized, 404 Not Found, 500 Internal Server Error).
*   Error responses will include a JSON object with a descriptive error message.  Example: `{ "message": "Invalid username or password" }`

## 7. User Interface (UI)

The UI will be designed with simplicity and usability in mind.  Key screens include:

*   **Login/Registration:**  Forms for user login and registration.
*   **Task List:**  Displays a list of tasks, sorted by due date.  Includes controls for creating, editing, deleting, and marking tasks as complete.
*   **Task Details (Optional - May be combined with Task List):** A view for displaying and editing the details of a specific task.
*   **User Profile:**  Allows users to view and edit their profile information (name, email, reminder preference).

## 8. Email Reminders

*   **Trigger:**  A scheduled job (e.g., using a library like `schedule` or a task queue like Celery, *although for the MVP, a simple scheduled check within the Flask app might suffice*) will periodically check for tasks that are due to have reminders sent.
*   **Content:**  The email will include the task title, description, due date, and due time.
*   **Provider:**  One of the supported email providers (Mailgun, SendGrid, Amazon SES) will be used via the Flask-Mail extension.
*    **Testing:** During development, email sending will be mocked to avoid sending real emails.

## 9. Development Process

*   **Version Control:** Git (with GitHub, GitLab, or Bitbucket).
*   **Branching Strategy:**  A feature branch workflow will be used (create a new branch for each feature or bug fix).
*   **Code Style:**  Follow PEP 8 for Python code.  Use a consistent style guide for JavaScript and CSS.
*   **Testing:**  Write unit tests (using `pytest` or a similar framework) for the backend API and React components.
*   **Agile Methodology:** Use an iterative development approach, with short sprints (e.g., 1-2 weeks).

## 10. Deployment

*   **Platform:** PythonAnywhere.
*   **Steps:**
    1.  Create a PythonAnywhere account.
    2.  Upload the code (via Git or directly).
    3.  Set up a virtual environment and install dependencies.
    4.  Create the database (PostgreSQL or MySQL) and run migrations (using Flask-Migrate, which integrates with Flask-SQLAlchemy).
    5.  Configure environment variables (database connection string, email API key, secret key for Flask).
    6.  Configure the WSGI file.
    7.  Start the web application.

## 11. Future Enhancements (Beyond MVP)

This section lists potential features for future development, as outlined in the original proposal:

*   Recurring Tasks.
*   Task Categories/Projects.
*   Advanced Task Filtering and Sorting.
*   Task Assignment and Collaboration.
*   Calendar Integration.
*   Progress Tracking and Statistics.
*   Integrations with other productivity tools.
*   Improved Accessibility Features.
* Focus mode.
* Eisenhower Matrix.

## 12. Open Issues/Risks

*   **Email Deliverability:**  Ensuring that email reminders are not marked as spam. This may require configuring SPF, DKIM, and DMARC records.
*   **Scalability:**  While the MVP is designed for a small number of users, the architecture should be designed with scalability in mind. Database performance and the efficiency of the reminder scheduling mechanism will be important considerations for future growth.
*   **Security:**  Regular security reviews and updates will be necessary to protect user data.
*  **Time estimation:** Need to estimate time required to perform each task.

## 13. Appendix

*   **Example Flask-SQLAlchemy Models (models.py):**

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('UserProfile', backref='user', uselist=False)  # One-to-one
    tasks = db.relationship('Task', backref='user', lazy=True) # One-to-many

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    name = db.Column(db.String(80))
    reminder_preference = db.Column(db.String(20), nullable=False) #e.g., "1 hour", "1 day"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<UserProfile for User ID {self.user_id}>'

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    due_time = db.Column(db.Time, nullable=False)
    is_complete = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Task {self.title}>'
