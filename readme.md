# Chatylon

Simple server-rendered chat app.

![Chatylon user list](screenshot.png)

## Dependencies
- Django
- psycopg2
- django-crispy-forms
- django-debug-toolbar
- django-model-utils
- python-decouple

## Instructions

1. Build the containers:
> docker-compose build

2. Edit and rename default .env:
> docker-compose run web mv .default_env .env

3. Run Django migrations:
> docker-compose run web python manage.py migrate

4. Launch all containers:
> docker-compose up