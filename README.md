# Student Portal
# RENDER Link - 
https://student-portal-bteu.onrender.com

# Github Link - 
https://github.com/colin-182/student-portal


A Django-based student portal that allows authenticated users to manage projects, communicate with other users, and manage their profile information.

## Project Overview

The Student Portal provides a central web application for students to manage project information and communicate with other users.

The application includes authentication, project management, user profiles, and an internal messaging system.

The application is built with Django and uses PostgreSQL in production.

## Features

### User Accounts

- User registration
- User login and logout
- Password change
- Password reset
- Profile viewing
- Profile editing
- User authentication and access control

### Dashboard

The dashboard provides an overview of the user's activity, including:

- Number of projects
- Total received messages
- Unread messages
- Recent projects
- Recent messages

### Project Management

Authenticated users can:

- Create projects
- View their projects
- View individual project details
- Edit projects
- Delete projects
- Set project status
- Set project start and end dates
- Add project stakeholders

Project ownership is enforced so users can only manage their own projects.

### Messaging

Authenticated users can:

- Send messages
- View their inbox
- View sent messages
- View archived messages
- Open messages
- Reply to received messages
- Archive messages
- Restore archived messages
- Delete received messages

Messages are protected so users can only access messages they sent or received.

## Technologies

- Python
- Django
- PostgreSQL
- SQLite for local development where configured
- HTML
- CSS
- JavaScript
- Gunicorn
- WhiteNoise
- Pillow
- python-dotenv
- Git
- GitHub
- Render

## Project Structure

```text
student-portal/
│
├── accounts/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── dashboard/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── messaging/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── projects/
│   ├── migrations/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   ├── images/
│   └── js/
│
├── templates/
│   ├── includes/
│   └── registration/
│
├── manage.py
├── requirements.txt
└── README.md

## Deployment

The application is configured for deployment on Render using the included
`render.yaml` file.

### Deploying to Render

1. Push the project to GitHub.
2. Create a new Render Blueprint.
3. Connect the GitHub repository.
4. Render will use `render.yaml` to create:
   - The Student Portal web service.
   - A PostgreSQL database.
5. Add the required environment variables in Render:
   - `SECRET_KEY`
   - `ALLOWED_HOSTS`
   - `CSRF_TRUSTED_ORIGINS`
   - `EMAIL_HOST_USER`
   - `EMAIL_HOST_PASSWORD`
   - `DEFAULT_FROM_EMAIL`
6. Deploy the application.
7. Render automatically installs dependencies, collects static files,
   applies database migrations, and starts the application using Gunicorn.

### Accessing the Application

Live application:

https://student-portal-bteu.onrender.com

GitHub repository:

https://github.com/colin-182/student-portal
