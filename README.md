# Django and Flask Session Management
This repository provides sample code for session management using Django and Flask frameworks with Redis as the session storage backend.

## Django
The Django code is located in the django_app directory. It includes the following files:

* settings.py: Django settings file where session-related configurations are defined.
* views.py: Contains the views for login, main, and logout functionality.
* login.html and main.html: HTML templates for the login and main pages.

### To run the Django application:

1. Make sure you have Redis installed and running on your local machine.
2. Install the required dependencies by running pip install -r requirements.txt.
3. Start the Django development server with python manage.py runserver.
4. Access the application in your browser at http://localhost:8000.

## Flask

The Flask code is located in the flask_app directory. It includes the following files:

* app.py: Flask application file where session-related configurations are set up.
* templates/login.html and templates/main.html: HTML templates for the login and main pages.

### To run the Flask application:

1. Make sure you have Redis installed and running on your local machine.
2. Install the required dependencies by running pip install -r requirements.txt.
3. Start the Flask development server with python app.py.
4. Access the application in your browser at http://localhost:5000.