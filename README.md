# Yatube API
### Description
Yatube is a platform designed for authors, providing a range of features that include:

- Posting and browsing publications
- Commenting on publications
- Subscribing to authors for regular updates.

This repository contains only the API part of the project.

### Tech stack
1. Python 3.7.5
2. Django 2.2.16
3. Django Rest Framework
4. JWT + Djoser
5. Dotenv

### How to run the project
To run the project, follow these steps:

Clone the repository to your computer using the git clone command.
```
git clone https://github.com/ilyakhakhalkin/api_final_yatube.git
```

Go to the project directory in terminal:
```
cd api_final_yatube
```

Create and activate virtual environment:
```
python3 -m venv venv
```
```
source venv/bin/activate
```

Install dependencies from requirements.txt:
```
python3 -m pip install --upgrade pip
```
```
pip install -r requirements.txt
```

Run migrations:
```
python3 manage.py migrate
```

Run dev server:
```
python3 manage.py runserver
```

When you run the project, the documentation for the Yatube API will be available at http://127.0.0.1:8000/redoc/. The documentation explains how our API works and is presented in the Redoc format.

### ReadOnly access:
Unauthenticated users have read-only access, meaning they can make the following requests:
```
GET: api/v1/posts/ - request for all publications
GET: api/v1/posts/{id}/ - request for a specific publication by its ID

GET: api/v1/groups/ - request for all groups
GET: api/v1/groups/{id}/ - request for a specific group by its ID

GET: api/v1/{post_id}/comments/ - request for all comments on a publication
GET: api/v1/{post_id}/comments/{id}/ - request for a specific comment by its ID on a publication
```

### Authentication
Authentication is only available to registered users.
To register, you need to create a superuser account by following these steps:
```
python3 manage.py createsuperuser
```

Regular user registration is available to superusers through the Django admin panel.

Authentication is done using a JWT token.
To create a new token, you need to pass the username and password by following these steps:
```
{
    "username": "username",
    "password": "password"
}

POST: api/v1/jwt/create/
```
