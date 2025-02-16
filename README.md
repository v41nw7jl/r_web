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
